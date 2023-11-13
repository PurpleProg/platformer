import pygame.display
from background import Background
import gamestate
from fonctions import *
from player import Player
from tile import *


class Level:
    def __init__(self, level_num: int, spritesheet: str, character_name: str, gravity: int, game_state_manager: gamestate.GameStateManager):

        # assertions
        assert character_name in CHAR_LIST, f"{character_name} not in CHAR_LIST"

        self.surface = pygame.display.get_surface()
        self.background_sky = Background()
        self.spritesheet = get_spritesheet(spritesheet, False)
        self.character = load_character(character_name)
        self.gravity = gravity

        self.game_state_manager = game_state_manager
        self.playing = True         # for pause / unpause
        self.running = True         # for ending the level
        self.level_num = level_num
        self.x_shift = 0
        self.y_shift = 0

        # define groups for tiles
        self.player_group = DefaultGroup()
        self.visibles = DefaultGroup()      # group visibles is drawn
        self.all = DefaultGroup()           # group all is used for updates

        # loading tiles
        #
        # loading them in the right order is tricky, especially for the player
        # because he appends in the misc file but need to be added to visible at the same time as hidden
        for path in level_files_path(level_num):
            level_csv = import_csv(path)

            # define the group for each file
            group_name = path[path.rfind('_')+1:(path.rfind('.'))]  # extract just a name from the path
            exec(f"self.{group_name} = DefaultGroup()")

            # loading each tile into it group
            for row_index, row in enumerate(level_csv):
                for col_index, id in enumerate(row):
                    pos = (col_index*TILE_SIZE, row_index*TILE_SIZE)
                    if id != '-1':          # id -1 mean there is nothing at this place
                        tile = Tile(pos, id, self.spritesheet)
                        if group_name == 'misc':
                            if id == '50':      # 50 is the id of the player
                                self.player = Player(pos, self.character)
                                self.player_group.add(self.player)
                            else:
                                exec(f"self.{group_name}.add(tile)")
                                self.all.add(tile)
                        else:
                            exec(f"self.{group_name}.add(tile)")
                            self.all.add(tile)
            if group_name != 'hidden':
                exec(f"self.visibles.add(self.{group_name})")
            else:
                # groupe_name == hidden
                # time to add player to visibles
                self.visibles.add(self.player_group)

        self.player.x_shift_speed = self.player.speed_x

    def run(self, dt: float):

        # updates
        self.background_sky.update()
        self.update()   # change x_shift et y_shift en fonction de la position de player
        self.player.update(dt)    # change la direction + anime

        # update x
        self.all.update_x(self.x_shift, self.player.x_shift_speed, dt)     # applique x_chift
        self.player.move_x(dt)
        self.collide_x()                # replace sur X si collision

        # update y
        self.all.update_y(self.y_shift, dt)          # applique y_chift
        self.player.move_y(self.gravity, dt, self.y_shift)    # applique la gravité et le saut
        self.collide_y()                # replace sur Y si collision

        # draw groups
        self.visibles.draw(self.surface)
        self.collide_hidden()               # draw hidden group only if there is no collision

        # items and end flag
        self.collide_misc()

    def update(self):
        """Si le joueur s'approche du bord, immobilise le et bouge les tuiles dans le sens inverse
        les tuiles ne sont pas deplacees ici,
        seulement une variable shift est modifiee puis sera utilisee par la fonction update des tuiles"""
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
        """fin du jeux si on gagne"""
        # reset groups
        self.hidden.empty()
        self.all.empty()
        self.visibles.empty()

        self.running = False

        self.level_num += 1
        if self.level_num >= self.game_state_manager.states['mainmenu'].max_level:
            self.game_state_manager.set_state('cutscene')
        else:
            self.game_state_manager.set_state('mainmenu')

    def game_over(self):
        """end game if die"""
        # reset groups
        self.all.empty()
        self.hidden.empty()
        self.visibles.empty()

        self.running = False

        self.game_state_manager.set_state('mainmenu')

    def collide_y(self):
        """gere toutes les collisions sur l'axe Y (pour les tuiles et les ponds)"""
        # collide with tiles
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(self.player.rect):
                # top
                if self.player.vecteur.y < 0:  # using vecteur instead of direction because gravity mess up direction
                    self.player.rect.top = sprite.rect.bottom
                    self.player.pos.y = sprite.rect.bottom
                    self.player.direction.y = 1.0
                # bottom
                elif self.player.vecteur.y > 0:
                    self.player.rect.bottom = sprite.rect.top
                    self.player.pos.y = sprite.rect.top - TILE_SIZE
                    self.player.anim_is_jumping = False
                    self.player.direction.y = 0
                self.player.vecteur.y = 0

        # collide with the bridges
        for sprite in self.bridges.sprites():
            if sprite.rect.colliderect(self.player.rect):
                if self.player.direction.y == 1.0:
                    if (self.player.rect.bottom - sprite.rect.top) < TOLERANCE_POND:
                        self.player.rect.bottom = sprite.rect.top
                        self.player.pos.y = sprite.rect.top - TILE_SIZE
                        self.player.anim_is_jumping = False
                        self.player.direction.y = 0
                        self.player.vecteur.y = 0

        # death
        if self.player.rect.y > 3000:
            self.game_over()

    def collide_x(self):
        """gere toutes les collisions sur l'axe X"""
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(self.player.rect):
                # left
                if self.player.direction.x < 0:
                    self.player.pos.x = sprite.rect.right
                    self.player.rect.left = sprite.rect.right
                # right
                elif self.player.direction.x > 0:
                    self.player.pos.x = sprite.rect.left - TILE_SIZE
                    self.player.rect.right = sprite.rect.left

    def collide_misc(self):
        """gere les collisions avec les items"""
        # get the points and increment score
        if pygame.sprite.spritecollide(self.player, self.misc, False):
            collided = pygame.sprite.spritecollide(self.player, self.misc, False, pygame.sprite.collide_mask)
            if collided:
                if collided[0].id == 261:       # 261 is the id of the big golden ball (from the tiled map)
                    self.player.score += 5
                    collided[0].kill()
                elif collided[0].id == 262:     # 262 is the id of the small golden ball (from the tiled map)
                    self.player.score += 1
                    collided[0].kill()
                elif collided[0].id == 25:      # 25 is the id of the end flag (from the tiled map)
                    self.game_finish()

    def collide_hidden(self):
        """draw the hidden group only if there is no collision with the player"""
        if not pygame.sprite.spritecollide(self.player, self.hidden, False):
            self.hidden.draw(self.surface)
