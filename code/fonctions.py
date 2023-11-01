from csv import reader
import pygame
from settings import *


def import_csv(path: str):
    """import a csv file from a path
    return a 2d list of IDs of tiles
    IDs corresponds to the sprite position on the spritesheet"""

    assert path[-4:] == '.csv', f"no a csv file ({path[-4:]})"

    level_map_list = []
    with open(path) as data_map:
        level_data = reader(data_map)
        for row in level_data:
            level_map_list.append(list(row))
        # return a 2D list
        return level_map_list


def get_pos_from_id(tile_id: int):
    """calculate the position of the sprite on the spritesheet from an ID"""
    x = tile_id % 25        # modulo
    y = tile_id // 25       # reste de la division euclidienne
    return x, y


def load_character(character: str):
    """load an image of a given character from his name (and the const CHAR_LIST)
    return a image (type surf)"""
    assert character in CHAR_LIST, f"{character} not in CHAR_LIST"
    loaded_character = (
        pygame.image.load(f'../images/NinjaAdventure/Actor/Characters/{character}/SpriteSheet.png').convert_alpha()
    )
    return loaded_character


def level(num: int):
    """return a list of path for a given level num"""
    # devrait etre evolutif en fonction du contenu du fichier level/ et de l'extension du fichier
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
    """return a spritesheet image"""

    if animated is True:
        path = f'../images/NinjaAdventure/Backgrounds/Animated/{name}.png'
    else:
        path = f'../images/NinjaAdventure/Backgrounds/Tilesets/{name}.png'
    spritesheeet = pygame.image.load(path).convert_alpha()
    # return a image
    return spritesheeet


def render_text(text: str, size: int, color: tuple):
    """return a image from a text, a size and a color """
    # assertions
    assert len(color) == 3, f'expects 3, got {len(color)}'

    pygame.font.init()
    font = pygame.font.SysFont(pygame.font.get_default_font(), size)
    return font.render(text, True, color)
