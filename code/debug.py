import pygame


def debug(info):
    info = str(info)
    display = pygame.display.get_surface()
    font = pygame.font.Font(pygame.font.get_default_font(), 30)
    text = font.render(info, False, (255, 255, 255))
    surf = pygame.Surface(text.get_size())
    surf.fill((0, 0, 0))
    surf.blit(text, (0, 0))
    display.blit(surf, (10, 10))
