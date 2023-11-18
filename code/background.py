import pygame
from fonctions import get_full_path
import os


class Background:
    """images displayed on the background_sky"""
    def __init__(self, level_num: int):
        self.game_display = pygame.display.get_surface()

        # creating one surface from multiples background_sky images
        for _, _, files in os.walk(get_full_path(f'level/{level_num}/background/')):
            bg_images = files
            break

        self.surf = pygame.Surface(pygame.display.get_desktop_sizes()[0])

        for image in bg_images:
            image = pygame.image.load(get_full_path(f'level/{level_num}/background/{image}')).convert_alpha()
            image = pygame.transform.scale(image, pygame.display.get_desktop_sizes()[0])
            rect = image.get_rect()
            self.surf.blit(image, rect)

        self.rect = self.surf.get_rect()

    def update(self):
        """blit the background_sky on the display"""
        self.game_display.blit(self.surf, self.rect)
