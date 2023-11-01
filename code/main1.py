import pygame
from menus import *
from gamestate import GameStateManager
import time
from debug import debug


class Game:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        # setting up the windows
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('platformer')
        icon = pygame.Surface((10, 10))
        icon.fill((0, 0, 0))
        pygame.display.set_icon(icon)

        self.game_state_manager = GameStateManager()

        self.level_num = settings.level_num
        self.main_menu = Mainmenu(self.game_state_manager)
        self.game_state_manager.states['mainmenu'] = self.main_menu
        self.game_state_manager.states['level'] = Runlevel(self.level_num, self.game_state_manager)

    def run(self):
        prev_time = time.time()
        while True:
            # define delta time
            dt = time.time() - prev_time
            prev_time = time.time()

            # debugging frame rate
            try:
                frame_rate = int(1/dt)
            except ZeroDivisionError:  # on the first frame dt = 0
                frame_rate = FPS

            self.game_state_manager.states[self.game_state_manager.get_state()].run(dt)

            debug(frame_rate)

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
