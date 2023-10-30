import pygame
from fonctions import get_x_y_from_id
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, tile_id: str, spritesheet):
        super().__init__()

        # assertions
        assert len(pos) == 2, f'expects 2, got {len(pos)}'
        assert str(type(spritesheet)) == "<class 'pygame.surface.Surface'>", f"expects <class 'pygame.surface.Surface'>, got {str(type(spritesheet))} instead"

        self.id = int(tile_id)    # typecast from str to int
        load_pos = get_x_y_from_id(self.id)
        self.image = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
        self.image.blit(
            spritesheet, (0, 0), (load_pos[0]*SPRITE_SIZE, load_pos[1]*SPRITE_SIZE, SPRITE_SIZE, SPRITE_SIZE)
        )
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)

    def update_x(self, x_shift: int):
        assert x_shift in (-1, 0, 1), f"expects -1, 0 or 1; got {x_shift} "
        self.rect.x += x_shift * SPEED

    def update_y(self, y_shift: int):
        assert y_shift in (-1, 0, 1), f"expects -1, 0 or 1; got {y_shift} "
        self.rect.y += y_shift * SPEED


class DefaultGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def update_x(self, x_shift: int, speed: int, dt: float):
        assert x_shift in (-1, 0, 1), f"expects -1, 0 or 1; got {x_shift} "
        for sprite in self:
            sprite.rect.x += x_shift * speed * dt

    def update_y(self, y_shift: int, dt: float):
        assert y_shift in (-1, 0, 1), f"expects -1, 0 or 1; got {y_shift} "
        for sprite in self:
            sprite.rect.y += y_shift * SPEED * dt
