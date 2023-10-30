import pygame.display

import settings
from background import Background
from fonctions import *
from player import Player
from tile import *


class Level:
    def __init__(self, load_level_num: int, spritesheet, character: str, gravity: int, game_state_manager):

        # assertions
        assert str(type(spritesheet)) == "<class 'str'>", f"expects <class 'str'>, got {str(type(spritesheet))} instead"
        assert character in CHAR_LIST, f"{character} not in CHAR_LIST"
        assert str(type(game_state_manager)) == "<class 'gamestate.GameStateManager'>", f"expects <class 'gamestate.GameStateManager'>, got {str(type(game_state_manager))} instead"

        self.surface = pygame.display.get_surface()
        self.background = Background()
        self.spritesheet = get_spritesheet(spritesheet, False)
        self.character = load_character(character)
        self.gravity = gravity

        self.game_state_manager = game_state_manager
        self.playing = True
        self.x_shift = 0
        self.y_shift = 0

        # define groups for tiles
        self.collidibles = DefaultGroup()
        self.background_group = DefaultGroup()
        self.top_tile = DefaultGroup()
        self.misc_group = DefaultGroup()
        self.player_group = DefaultGroup()
        self.foreground = DefaultGroup()
        self.visibles = DefaultGroup()
        self.grass = DefaultGroup()
        self.bridges = DefaultGroup()
        self.hidden = DefaultGroup()

        # loading tiles
        for data in level(load_level_num):
            level_csv = import_csv(data)

            for row_index, row in enumerate(level_csv):
                for col_index, case in enumerate(row):
                    pos = (col_index*TILE_SIZE, row_index*TILE_SIZE)
                    if case != '-1':
                        tile = Tile(pos, case, self.spritesheet)
                        if data == f'../level/{load_level_num}._tiles.csv':
                            self.collidibles.add(tile)
                        elif data == f'../level/{load_level_num}._misc.csv':
                            if case == '50':
                                self.player = Player(pos, self.character)
                                self.player_group.add(self.player)
                            else:
                                self.misc_group.add(tile)
                        elif data == f'../level/{load_level_num}._background.csv':
                            self.background_group.add(tile)
                        elif data == f'../level/{load_level_num}._toptile.csv':
                            self.top_tile.add(tile)
                        elif data == f'../level/{load_level_num}._foreground.csv':
                            self.foreground.add(tile)
                        elif data == f'../level/{load_level_num}._grass.csv':
                            self.grass.add(tile)
                        elif data == f'../level/{load_level_num}._bridges.csv':
                            self.bridges.add(tile)
                        elif data == f'../level/{load_level_num}._hidden.csv':
                            self.hidden.add(tile)
                        # else:
                        #     self.visibles.add(tile)

        self.player.x_shift_speed = self.player.speed_x

        # setting up visibles group (only him is draw)
        self.visibles.add(self.background_group)
        self.visibles.add(self.collidibles)
        self.visibles.add(self.bridges)
        self.visibles.add(self.top_tile)
        self.visibles.add(self.misc_group)
        self.visibles.add(self.grass)
        self.visibles.add(self.player_group)
        self.visibles.add(self.foreground)

    def run(self, dt: float):

        # updates
        self.background.update()
        self.update()   # change x_shift et y_shift en fonction de la position de player
        self.player.update(dt)    # change la direction + anime

        # update x
        self.visibles.update_x(self.x_shift, self.player.x_shift_speed, dt)     # applique x_chift
        self.hidden.update_x(self.x_shift, self.player.x_shift_speed, dt)
        self.player.move_x(dt)
        self.collide_x()                # replace sur Y si besoin

        # update y
        self.visibles.update_y(self.y_shift, dt)
        self.hidden.update_y(self.y_shift, dt)
        self.player.move_y(self.gravity, dt, self.y_shift)    # applique la gravité et le saut
        self.collide_y()                # replace sur Y si besoin

        # draw groups
        self.visibles.draw(self.surface)
        self.collide_hidden()               # draw hidden group only if there is no collision

        # items
        self.collide_misc()

    def update(self):
        if self.player.rect.right > WIDTH-BORDURE and self.player.direction.x > 0:
            self.x_shift = -1
            self.player.speed_x = 0
        elif self.player.rect.left < BORDURE and self.player.direction.x < 0:
            self.x_shift = 1
            self.player.speed_x = 0
        else:
            self.x_shift = 0
            self.player.speed_x = SPEED

        if self.player.rect.top < TOP_BORDURE:
            self.y_shift = 1
            self.player.speed_y = 0
        elif self.player.rect.bottom > HEIGHT-BOTTOM_BORDURE:
            self.y_shift = -1
            self.player.speed_y = 0
        else:
            self.y_shift = 0
            self.player.speed_y = SPEED

    def game_finish(self):
        # reset groups
        self.hidden.empty()
        self.visibles.empty()

        settings.level_num += 1
        settings.score = self.player.score
        self.game_state_manager.set_state('mainmenu')

    def game_over(self):
        # reset groups
        self.hidden.empty()
        self.visibles.empty()

        settings.score = self.player.score
        self.game_state_manager.set_state('mainmenu')

    def collide_y(self):
        for sprite in self.collidibles.sprites():
            if sprite.rect.colliderect(self.player.rect):
                if self.player.vecteur.y < 0:  # using vecteur instead of direction because gravity mess up direction
                    self.player.rect.top = sprite.rect.bottom + 33000
                    self.player.pos.y = sprite.rect.bottom + 33090
                    self.player.direction.y = 1.0
                elif self.player.vecteur.y > 0:
                    self.player.rect.bottom = sprite.rect.top
                    self.player.pos.y = sprite.rect.top - TILE_SIZE
                    self.player.direction.y = 0
                self.player.vecteur.y = 0

        # collide with the bridges
        for sprite in self.bridges.sprites():
            if sprite.rect.colliderect(self.player.rect):
                if self.player.direction.y == 1.0:
                    if (self.player.rect.bottom - sprite.rect.top) < TOLERANCE_POND:
                        self.player.rect.bottom = sprite.rect.top
                        self.player.pos.y = sprite.rect.top - TILE_SIZE
                        self.player.direction.y = 0
                        self.player.vecteur.y = 0

        # death
        if self.player.rect.y > 3000:
            print('game over')
            self.game_over()

    def collide_x(self):
        for sprite in self.collidibles.sprites():
            if sprite.rect.colliderect(self.player.rect):
                if self.player.direction.x < 0:
                    self.player.pos.x = sprite.rect.right
                    self.player.rect.left = sprite.rect.right
                elif self.player.direction.x > 0:
                    self.player.pos.x = sprite.rect.left - TILE_SIZE
                    self.player.rect.right = sprite.rect.left

    def collide_misc(self):
        # get the points and increment score
        if pygame.sprite.spritecollide(self.player, self.misc_group, False):
            collided = pygame.sprite.spritecollide(self.player, self.misc_group, False, pygame.sprite.collide_mask)
            if collided:
                if collided[0].id == 261:
                    self.player.score += 5
                    collided[0].kill()
                elif collided[0].id == 262:
                    self.player.score += 1
                    collided[0].kill()
                elif collided[0].id == 25:
                    self.game_finish()

    def collide_hidden(self):
        if not pygame.sprite.spritecollide(self.player, self.hidden, False):
            self.hidden.draw(self.surface)
