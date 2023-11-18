import pygame


def debug(info, pos=(10, 10)):
    """show a variable on the screen"""

    # cast info to string
    info = str(info)

    # get the display
    display = pygame.display.get_surface()

    # get a surface from a string
    font = pygame.font.Font(pygame.font.get_default_font(), 30)
    text = font.render(info, False, (255, 255, 255))

    # creating a black background of the right size
    surf = pygame.Surface(text.get_size())
    surf.fill((0, 0, 0))

    # adding the text on the background
    surf.blit(text, (0, 0))

    # showing the result of all of the above on the screen
    display.blit(surf, pos)
