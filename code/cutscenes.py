import pygame
import sys
from settings import *
from fonctions import get_full_path, render_text


class Endscene:
    """end game cutscene"""
    def __init__(self):
        self.end_text = render_text('End.', 200, (0, 0, 0))
        self.screen = pygame.display.get_surface()

        self.end_text_pos_x = (WIDTH / 2) - self.end_text.get_rect().centerx
        self.end_text_pos_y = (HEIGHT / 2) - self.end_text.get_rect().centery

    def update(self, dt: float):
        self.screen.blit(self.end_text, (self.end_text_pos_x, self.end_text_pos_y))
        self.end_text_pos_y -= SPEED / 6 * dt
        if self.end_text_pos_y <= 0-self.end_text.get_rect().height:
            self.end_text_pos_y = HEIGHT
