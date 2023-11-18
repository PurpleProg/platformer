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

    def run(self):
        prev_time = time.time()
        while True:
            # define delta time
            dt = time.time() - prev_time
            prev_time = time.time()

            # run current state
            self.game_state_manager.states[self.game_state_manager.current_state].run(dt)

            debug(self.game_state_manager.states['level'].level.player.jumps)
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
