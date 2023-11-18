import pygame
from gamestate import GameStateManager
from states import *
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

        # defines game states
        self.game_state_manager = GameStateManager()
        self.game_state_manager.states['mainmenu'] = Mainmenu(self.game_state_manager)
        self.game_state_manager.states['level'] = Level_state(0,
                                                              self.game_state_manager.states['mainmenu'].char_num,
                                                              self.game_state_manager)
        self.game_state_manager.states['pause'] = Pause(self.game_state_manager.states['level'], self.game_state_manager)
        self.game_state_manager.states['cutscene'] = Cutscene()


    def run(self):
        prev_time = time.time()
        while True:
            # define delta time
            dt = time.time() - prev_time
            prev_time = time.time()

            # run current state
            self.game_state_manager.states[self.game_state_manager.get_state()].run(dt)

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
