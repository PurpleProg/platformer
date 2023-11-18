import sys
import typing

import pygame.display
from pygame.locals import *
from settings import *
import settings
from fonctions import render_text, get_full_path
from level import Level
from gamestate import GameStateManager


class Button:
    def __init__(self, pos: tuple, color: tuple, text: pygame.Surface, commande: typing.Callable):

        # assertions
        assert len(pos) == 2, f'expects 2, got {len(pos)}'
        assert len(color) == 3, f'expects 3, got {len(color)}'

        self.commande = commande
        self.image = pygame.Surface((200, 50))
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill(color)
        self.image.blit(text,
                        ((self.rect.w / 2) - (text.get_width() / 2), (self.rect.h / 2) - (text.get_height() / 2)))
        self.text = text

    def update(self, color):
        """sert a changer la couleur du bouton"""
        assert len(color) == 3, f'expects 3, got {len(color)}'
        self.image.fill(color)
        self.image.blit(self.text, (
            (self.rect.w / 2) - (self.text.get_width() / 2), (self.rect.h / 2) - (self.text.get_height() / 2)))

    def clicked(self):
        self.commande()


class ButtonsGroup:
    def __init__(self):
        self.buttons = []

    def add(self, button: Button):
        self.buttons.append(button)

    def update(self, color):
        """update the color of every button on the group"""
        assert len(color) == 3, f'expects 3, got {len(color)}'
        for button in self.buttons:
            button.update(color)

    def draw(self, surf: pygame.Surface):
        for button in self.buttons:
            surf.blit(button.image, button.rect)


class Mainmenu:
    def __init__(self, game_state_manager: GameStateManager):

        # configure the windows
        self.screen = pygame.display.get_surface()
        pygame.display.set_caption('platformer : main menu')
        self.screen.fill((0, 0, 0))
        self.icon = pygame.Surface((10, 10))
        self.icon.fill((0, 0, 255))
        pygame.display.set_icon(self.icon)

        self.game_state_manager = game_state_manager
        self.score = 0
        for _, dirs, _ in os.walk(get_full_path('level')):
            self.max_level = len(dirs)
            break

        # character selection image
        self.char_num = 9               # default 9 is blackninja
        self.char_face = pygame.image.load(
            get_full_path('images/NinjaAdventure/Actor/Characters/') + CHAR_LIST[self.char_num] + '\Faceset.png').convert()
        self.char_face = pygame.transform.scale(self.char_face, (200, 200))

        # creating buttons
        self.buttons = ButtonsGroup()
        self.buttons.add(Button((250, 500),   (100, 100, 100),
                                render_text('play', 50, (0, 0, 0)),
                                commande=self.play))
        self.buttons.add(Button((600, 500), (100, 100, 100),
                                render_text('replay', 50, (0, 0, 0)),
                                commande=self.replay))
        self.buttons.add(Button((800, 200), (100, 100, 100),
                                render_text('next char', 30, (0, 0, 0)),
                                commande=self.next_char))
        self.buttons.add(Button((100, 200), (100, 100, 100),
                                render_text('previous char', 30, (0, 0, 0)),
                                commande=self.prev_char))

    def run(self, dt: float):
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    self.next_char()
                elif event.key == K_LEFT:
                    self.prev_char()
                if event.key == K_RETURN:
                    self.play()
            for button in self.buttons.buttons:
                if button.rect.collidepoint(mouse):
                    button.update(BUTTON_COLOR_ON_MOUSE_OVER)
                    if event.type == MOUSEBUTTONDOWN:
                        button.clicked()
                else:
                    button.update(BUTTON_COLOR)

        self.screen.fill((0, 0, 0))

        self.buttons.draw(self.screen)
        self.screen.blit(self.char_face, (450, 100))
        self.screen.blit(render_text(f"level {self.game_state_manager.states['level'].level.level_num+1}",
                                     100, (255, 255, 255)), (450, 400))
        self.screen.blit(render_text(f"{CHAR_LIST[self.char_num]}", 80, (255, 255, 255)),
                         (450, 330))
        self.screen.blit(render_text(f"score : {self.game_state_manager.states['level'].level.player.score}",
                                     80, (255, 255, 255)), (450, 20))
        self.screen.blit(render_text(f"max level : {self.max_level+1}", 60,
                                     (255, 255, 255)), (100, 30))

    def play(self):
        """exit the menu and start the game"""
        self.game_state_manager.states['level'] = Runlevel(self.game_state_manager.states['level'].level.level_num,
                                                           self.char_num, self.game_state_manager)
        self.game_state_manager.set_state('level')

    def replay(self):
        """play the level current level instead of the next one"""
        if self.game_state_manager.states['level'].level.level_num > 0:
            self.game_state_manager.states['level'] = Runlevel(self.game_state_manager.states['level'].level.level_num - 1,
                                                               self.char_num, self.game_state_manager)
            self.game_state_manager.set_state('level')
        else:
            self.play()

    def next_char(self):
        """changing character"""
        if self.char_num == len(settings.CHAR_LIST) - 1:
            pass
        else:
            self.char_num += 1
        self.char_face = pygame.image.load(
            get_full_path('images/NinjaAdventure/Actor/Characters/') + CHAR_LIST[self.char_num] + '/Faceset.png').convert()
        self.char_face = pygame.transform.scale(self.char_face, (200, 200))

    def prev_char(self):
        """changing character"""
        if self.char_num == 0:
            pass
        else:
            self.char_num -= 1
        self.char_face = pygame.image.load(
            get_full_path('images/NinjaAdventure/Actor/Characters/') + CHAR_LIST[self.char_num] + '/Faceset.png').convert()
        self.char_face = pygame.transform.scale(self.char_face, (200, 200))


class Runlevel:
    def __init__(self, current_level_num: int, char_num: int, game_state_manager: GameStateManager):
        self.char_num = char_num
        self.level = Level(current_level_num, 'Assets', settings.CHAR_LIST[self.char_num], GRAVITY, game_state_manager)
        self.screen = pygame.display.get_surface()

        self.game_state_manager = game_state_manager

        # modifie la fenêtre
        pygame.display.set_caption('platformer : game')
        self.icon = pygame.Surface((10, 10))
        self.icon.fill((0, 0, 0))
        pygame.display.set_icon(self.icon)

        # cree les boutons
        self.buttons = ButtonsGroup()
        self.resume_button = Button((600, 500), (100, 100, 100),
                                    render_text('resume', 50, (0, 0, 0)),
                                    commande=self.resume)
        self.quit_button = Button((300, 500), (100, 100, 100),
                                  render_text('quit', 50, (0, 0, 0)),
                                  commande=self.quit)
        self.buttons.add(self.resume_button)
        self.buttons.add(self.quit_button)

    def resume(self):
        """exit pause"""
        self.level.playing = True

    def quit(self):
        """quit game and go to main menu"""
        self.game_state_manager.set_state('mainmenu')

    def run(self, dt: float):
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.level.player.jump(dt)
                if event.key == pygame.K_UP:
                    if self.level.player.jumps > 0:
                        self.level.player.jump(dt)

                if event.key == pygame.K_ESCAPE:
                    self.level.playing = not self.level.playing
                    surf = (pygame.Surface(pygame.display.get_desktop_sizes()[0]))
                    surf.set_alpha(200)
                    pygame.display.get_surface().blit(surf, (0, 0))
            if self.level.playing is False:      # pause
                for button in self.buttons.buttons:
                    if button.rect.collidepoint(mouse):
                        button.update(BUTTON_COLOR_ON_MOUSE_OVER)
                        if event.type == MOUSEBUTTONDOWN:
                            button.clicked()
                    else:
                        button.update(BUTTON_COLOR)
        if self.level.playing:
            self.level.run(dt)
            pygame.display.set_caption('platformer : game')
        else:       # si le niveau est en pause
            pygame.display.set_caption('platformer : paused')

            # pause screen
            paused_text = render_text('PAUSED', 200, (200, 200, 200))
            x = (WIDTH/2) - paused_text.get_rect().centerx
            y = (HEIGHT/2) - paused_text.get_rect().centery
            self.screen.blit(paused_text, (x, y))
            self.buttons.draw(self.screen)
