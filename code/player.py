import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, character: pygame.Surface):
        super().__init__()

        # assertions
        assert len(pos) == 2, f'expects 2, got {len(pos)}'
        assert character not in CHAR_LIST, "character not in CHAR_LIST"

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.direction = pygame.math.Vector2(0, 0)
        self.vecteur = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(pos)
        self.speed_x = SPEED
        self.speed_y = SPEED
        self.x_shift_speed = SPEED
        self.score = 0
        self.jumps = MAX_JUMPS

        # animation stuff
        self.counter = 0.0
        self.character = character
        self.anim_state = "idle"
        self.anim_is_jumping = False

    def update(self, dt: float):
        """Change la direction du joueur et l'anime"""

        # updating the y direction
        if self.vecteur.y > 0:
            self.direction.y = 1
        elif self.vecteur.y < 0:
            self.direction.y = 1

        self.animate(dt)

        # updating the x direction
        self.get_pressed()

    def animate(self, dt: float):
        """change the sprite of the player based on his current state"""
        # animations on X axis
        if self.anim_state == "idle":
            x = 0
            y = 0
        elif self.anim_state == "right":
            x = 3
            y = int(self.counter)
        elif self.anim_state == 'left':
            x = 2
            y = int(self.counter)
        # jumping animation
        if self.anim_is_jumping is True:          # rounded vecteur is == 0 at the top of the jump
            y = 5

        # couter
        self.counter += dt * AMINATION_SPEED * SPEED
        if int(self.counter) > 3:
            self.counter = 0

        self.get_sprite(self.character, (x, y))

    def get_sprite(self, sprite_sheet_image: pygame.Surface, pos: tuple):
        """called by the animate fonction.
        load the new player sprite from a spritesheet at the given position"""
        # assertions
        assert len(pos) == 2, f'expects 2, got {len(pos)}'

        self.image = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
        self.image.blit(sprite_sheet_image, (0, 0),
                        (pos[0] * SPRITE_SIZE, pos[1] * SPRITE_SIZE, SPRITE_SIZE, SPRITE_SIZE))
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def get_pressed(self):
        """change the x direction and the animation state based on key press"""

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.anim_state = "right"
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.anim_state = "left"
        else:
            self.direction.x = 0
            self.anim_state = "idle"

        # cheat
        if keys[pygame.K_r]:
            self.respawn(150, 150)

    def respawn(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y
        self.pos.x = x
        self.pos.y = y
        self.vecteur.y = 0
        self.direction.y = 0

    def gravity(self, gravity: int, dt: float):
        """apply the gravity"""
        self.vecteur.y += 0.5 * gravity * dt * dt
        self.direction.y = 1.0

    def move_x(self, dt: float):
        """move the player on x"""
        self.pos.x += self.direction.x * self.speed_x * dt
        self.rect.x = round(self.pos.x)

    def move_y(self, gravity: int, dt: float, y_shift: int):
        """move the player on y and call gravity"""

        self.gravity(gravity, dt)

        # replace to avoid super-jump du to tiles shift
        self.pos.y += y_shift * SPEED * dt

        # moving
        self.pos.y += self.vecteur.y
        self.rect.y = round(self.pos.y)

    def jump(self, dt: float):
        """set vecteur y to (JUMP * dt) and anim_is_jumping to True"""
        self.anim_is_jumping = True
        self.jumps -= 1

        self.vecteur.y = JUMP * dt

        self.pos.y += self.vecteur.y
        self.rect.y = round(self.pos.y)
