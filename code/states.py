import sys
import pygame
from settings import *
from fonctions import render_text, get_full_path, Button, ButtonsGroup
from level import Level
from cutscenes import *


class Mainmenu:
    def __init__(self, game_state_manager):

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
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.next_char()
                elif event.key == pygame.K_LEFT:
                    self.prev_char()
                if event.key == pygame.K_RETURN:
                    self.play()
            for button in self.buttons.buttons:
                if button.rect.collidepoint(mouse):
                    button.update(BUTTON_COLOR_ON_MOUSE_OVER)
                    if event.type == pygame.MOUSEBUTTONDOWN:
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
        self.game_state_manager.states['level'] = Level_state(self.game_state_manager.states['level'].level.level_num,
                                                              self.char_num, self.game_state_manager)
        self.game_state_manager.set_state('level')

    def replay(self):
        """play the level current level instead of the next one"""
        if self.game_state_manager.states['level'].level.level_num > 0:
            self.game_state_manager.states['level'] = Level_state(self.game_state_manager.states['level'].level.level_num - 1,
                                                               self.char_num, self.game_state_manager)
            self.game_state_manager.set_state('level')
        else:
            self.play()

    def next_char(self):
        """changing character"""
        if self.char_num == len(CHAR_LIST) - 1:
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


class Cutscene:
    def __init__(self):
        # cutscenes
        self.scene = Endscene()

        self.screen = pygame.display.get_surface()
        self.background = (pygame.Surface((WIDTH, HEIGHT)))
        self.background.fill((255, 255, 255))

    def run(self, dt: float):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.blit(self.background, (0, 0))
        self.scene.update(dt)


class Pause:
    def __init__(self, current_level: Level, game_state_manager):
        self.screen = pygame.display.get_surface()

        self.game_state_manager = game_state_manager
        self.level = current_level

        # modifie la fenêtre
        pygame.display.set_caption('platformer : pause')
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
        self.game_state_manager.set_state('level')
        # gamestate to level

    def quit(self):
        """quit game and go to main menu"""
        self.game_state_manager.set_state('mainmenu')

    def run(self, dt: float):
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.resume()

            for button in self.buttons.buttons:
                # button's command execution
                if button.rect.collidepoint(mouse):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        button.clicked()

        for button in self.buttons.buttons:
            # couleur des boutons a chaque frame
            if button.rect.collidepoint(mouse):
                button.update(BUTTON_COLOR_ON_MOUSE_OVER)
            else:
                button.update(BUTTON_COLOR)

            # draw pause screen
            paused_text = render_text('PAUSED', 200, (200, 200, 200))
            x = (WIDTH/2) - paused_text.get_rect().centerx
            y = (HEIGHT/2) - paused_text.get_rect().centery

            self.screen.blit(paused_text, (x, y))
            self.buttons.draw(self.screen)


class Level_state:
    def __init__(self, current_level_num: int, char_num: int, game_state_manager):
        self.char_num = char_num
        self.level = Level(current_level_num, 'Assets', CHAR_LIST[self.char_num], GRAVITY, game_state_manager)
        self.screen = pygame.display.get_surface()

        self.game_state_manager = game_state_manager

        # modifie la fenêtre
        pygame.display.set_caption('platformer : level')
        self.icon = pygame.Surface((10, 10))
        self.icon.fill((0, 0, 0))
        pygame.display.set_icon(self.icon)

    def run(self, dt: float):
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # jumps
                if event.key == pygame.K_SPACE:
                    # cheat
                    self.level.player.jump(dt)
                if event.key == pygame.K_UP:
                    # normal jump call
                    if self.level.player.jumps > 0:
                        self.level.player.jump(dt)

                if event.key == pygame.K_ESCAPE:

                    self.level.playing = False

                    self.game_state_manager.set_state('pause')

        self.level.run(dt)
