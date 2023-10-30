from csv import reader
import pygame
from settings import *


def import_csv(path: str):
    level_map_list = []
    with open(path) as data_map:
        level_data = reader(data_map)
        for row in level_data:
            level_map_list.append(list(row))
        # return a 2D list
        return level_map_list


def get_x_y_from_id(tile_id: int):
    x = tile_id % 25
    y = tile_id // 25
    return x, y


def load_character(character: str):
    assert character in CHAR_LIST, f"{character} not in CHAR_LIST"
    loaded_character = (
        pygame.image.load(f'../images/NinjaAdventure/Actor/Characters/{character}/SpriteSheet.png').convert_alpha()
    )
    # return a image
    return loaded_character


def level(num: int):
    return [
        f'../level/{num}._foreground.csv',
        f'../level/{num}._hidden.csv',
        f'../level/{num}._grass.csv',
        f'../level/{num}._misc.csv',
        f'../level/{num}._toptile.csv',
        f'../level/{num}._bridges.csv',
        f'../level/{num}._tiles.csv',
        f'../level/{num}._background.csv',
    ]


def get_spritesheet(name: str, animated: bool):

    if animated is True:
        path = f'../images/NinjaAdventure/Backgrounds/Animated/{name}.png'
    else:
        path = f'../images/NinjaAdventure/Backgrounds/Tilesets/{name}.png'
    spritesheeet = pygame.image.load(path).convert_alpha()
    # return a image
    return spritesheeet


def render_text(text: str, size: int, color: tuple):
    # assertions
    assert len(color) == 3, f'expects 3, got {len(color)}'

    pygame.font.init()
    font = pygame.font.SysFont(pygame.font.get_default_font(), size)
    return font.render(text, True, color)
