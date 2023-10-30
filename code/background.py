import pygame


class Background:
    def __init__(self):
        self.game_display = pygame.display.get_surface()
        self.image1 = pygame.image.load('../images/Tiles/Assets/Background_2.png').convert_alpha()
        self.image1 = pygame.transform.scale(self.image1, pygame.display.get_desktop_sizes()[0])
        self.rect1 = self.image1.get_rect()

        self.image2 = pygame.image.load('../images/Tiles/Assets/Background_1.png').convert_alpha()
        self.image2 = pygame.transform.scale(self.image2, pygame.display.get_desktop_sizes()[0])
        self.rect2 = self.image2.get_rect()

        self.surf = pygame.Surface(pygame.display.get_desktop_sizes()[0])
        self.surf.blit(self.image1, self.rect1)
        self.surf.blit(self.image2, self.rect2)
        self.rect = self.surf.get_rect()

    def update(self):
        self.game_display.blit(self.surf, self.rect)
