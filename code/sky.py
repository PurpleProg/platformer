import pygame
from settings import *


class Sky:
    def __init__(self):
        self.game_surf = pygame.display.get_surface()
        self.overlay_surf = (pygame.Surface((WIDTH, HEIGHT)))
        self.overlay_surf.fill((0, 0, 0))
        self.overlay_surf.set_alpha(128)

    def dark(self):
        self.overlay_surf.set_alpha(138)
        pygame.display.get_surface().blit(self.overlay_surf, (0, 0))
