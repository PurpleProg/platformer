import os
from fonctions import get_full_path

# general
FPS = 60
TILE_SIZE = 64
WIDTH = 1200
HEIGHT = TILE_SIZE * 10
SPEED = 500
TOP_BORDURE = TILE_SIZE * 2
BOTTOM_BORDURE = TILE_SIZE * 4

# player
CHAR_LIST = os.listdir(get_full_path('images/NinjaAdventure/Actor/Characters/'))
BORDURE = TILE_SIZE * 5
SPRITE_SIZE = 16
JUMP = -1200
GRAVITY = 6500
TOLERANCE_POND = TILE_SIZE / 2
AMINATION_SPEED = 0.015
MAX_JUMPS = 2

BUTTON_COLOR = (200, 200, 200)
BUTTON_COLOR_ON_MOUSE_OVER = (100, 100, 100)
