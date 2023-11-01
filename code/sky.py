import pygame
from settings import *


class Sky:
    """transparents overlays of the game"""
    def __init__(self):
        self.game_surf = pygame.display.get_surface()
        self.overlay_surf = (pygame.Surface((WIDTH, HEIGHT)))
        self.overlay_surf.fill((0, 0, 0))

    def dark(self):
        """Ajoute une couche de gris transparent au-dessus du jeu"""
        self.overlay_surf.set_alpha(138)
        pygame.display.get_surface().blit(self.overlay_surf, (0, 0))
