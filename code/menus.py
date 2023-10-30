import pygame.display
from pygame.locals import *
from settings import *
import settings
from fonctions import render_text
from level import Level


class Button:
    def __init__(self, pos: tuple, color: tuple, text, commande):

        # assertions
        assert len(pos) == 2, f'expects 2, got {len(pos)}'
        assert len(color) == 3, f'expects 3, got {len(color)}'
        assert str(type(text)) == "<class 'pygame.surface.Surface'>", f"expects <class 'pygame.surface.Surface'>, got {str(type(text))} instead"
        assert str(type(commande)) == "<class 'method'>", f"expects <class 'method'>, got {str(type(text))} instead"

        self.commande = commande
        self.image = pygame.Surface((200, 50))
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill(color)
        self.image.blit(text,
                        ((self.rect.w / 2) - (text.get_width() / 2), (self.rect.h / 2) - (text.get_height() / 2)))
        self.text = text

    def update(self, color):
        assert len(color) == 3, f'expects 3, got {len(color)}'
        self.image.fill(color)
        self.image.blit(self.text, (
            (self.rect.w / 2) - (self.text.get_width() / 2), (self.rect.h / 2) - (self.text.get_height() / 2)))

    def clicked(self):
        self.commande()


class ButtonsGroup:
    def __init__(self):
        self.buttons = []

    def add(self, button):
        assert str(type(button)) == "<class 'menus.Button'>", f"expects <class 'menus.Button'>, got {str(type(button))}"
        self.buttons.append(button)

    def update(self, color):
        assert len(color) == 3, f'expects 3, got {len(color)}'
        for button in self.buttons:
            button.update(color)

    def draw(self, surf):
        assert str(type(surf)) == "<class 'pygame.surface.Surface'>", f"expects <class 'pygame.surface.Surface'>, got {str(type(surf))} instead"
        for button in self.buttons:
            surf.blit(button.image, button.rect)


class Mainmenu:
    def __init__(self, game_state_manager):
        assert str(type(game_state_manager)) == "<class 'gamestate.GameStateManager'>", f"expects <class 'gamestate.GameStateManager'>, got {str(type(game_state_manager))} instead"

        # configure the windows
        self.screen = pygame.display.get_surface()
        pygame.display.set_caption('platformer : main menu')
        self.screen.fill((0, 0, 0))
        self.icon = pygame.Surface((10, 10))
        self.icon.fill((0, 0, 255))
        pygame.display.set_icon(self.icon)

        self.game_state_manager = game_state_manager

        settings.char_face = pygame.image.load(
            '../images/NinjaAdventure/Actor/Characters/' + CHAR_LIST[settings.char_num] + '/Faceset.png').convert()
        settings.char_face = pygame.transform.scale(settings.char_face, (200, 200))

        # buttons
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
                quit()
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
            self.screen.blit(settings.char_face, (450, 100))
            self.screen.blit(render_text(f'level {settings.level_num+1}', 100, (255, 255, 255)), (450, 400))
            self.screen.blit(render_text(f'{settings.CHAR_LIST[settings.char_num]}', 80, (255, 255, 255)), (450, 330))
            self.screen.blit(render_text(f'score : {int(settings.score)}', 80, (255, 255, 255)), (450, 20))

    def play(self):
        self.game_state_manager.states['level'] = Runlevel(settings.level_num, self.game_state_manager)
        self.game_state_manager.set_state('level')

    def replay(self):
        if settings.level_num > 0:
            last_level_num = settings.level_num - 1
            self.game_state_manager.states['level'] = Runlevel(settings.level_num - 1, self.game_state_manager)
            self.game_state_manager.set_state('level')
            settings.level_num = last_level_num

    def next_char(self):

        if settings.char_num == len(settings.CHAR_LIST) - 1:
            pass
        else:
            settings.char_num += 1
        settings.char_face = pygame.image.load(
            '../images/NinjaAdventure/Actor/Characters/' + CHAR_LIST[settings.char_num] + '/Faceset.png').convert()
        settings.char_face = pygame.transform.scale(settings.char_face, (200, 200))

    def prev_char(self):

        if settings.char_num == 0:
            pass
        else:
            settings.char_num -= 1
        settings.char_face = pygame.image.load(
            '../images/NinjaAdventure/Actor/Characters/' + CHAR_LIST[settings.char_num] + '/Faceset.png').convert()
        settings.char_face = pygame.transform.scale(settings.char_face, (200, 200))


class Runlevel:
    def __init__(self, current_level_num: int, game_state_manager):
        assert str(type(game_state_manager)) == "<class 'gamestate.GameStateManager'>", f"expects <class 'gamestate.GameStateManager'>, got {str(type(game_state_manager))} instead"
        self.level = Level(f'level-{current_level_num}', 'Assets', settings.CHAR_LIST[settings.char_num], GRAVITY, game_state_manager)
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
        self.level.playing = True

    def quit(self):
        self.game_state_manager.set_state('mainmenu')

    def run(self, dt: float):
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
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
