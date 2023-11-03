import os

# variables globales
char_num = 9            # par default
char_face = None
score = 0
level_num = 0

# constantes
CHAR_LIST = os.listdir('../images/NinjaAdventure/Actor/Characters/')
FPS = 60
TILE_SIZE = 64
WIDTH = 1200
HEIGHT = TILE_SIZE * 10
SPEED = 500
BORDURE = TILE_SIZE * 5
TOP_BORDURE = TILE_SIZE * 2
BOTTOM_BORDURE = TILE_SIZE * 4
JUMP = -1200
GRAVITY = 6500
SPRITE_SIZE = 16
TOLERANCE_POND = TILE_SIZE / 2
AMINATION_SPEED = 0.015
BUTTON_COLOR = (200, 200, 200)
BUTTON_COLOR_ON_MOUSE_OVER = (100, 100, 100)
