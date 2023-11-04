import os.path
import sys
from csv import reader
import pygame
import settings


def import_csv(path: str):
    """import a csv file from a path
    return a 2d list of IDs of tiles
    IDs corresponds to the sprite position on the spritesheet"""

    assert path[-4:] == '.csv', f"no a csv file ({path[-4:]})"

    level_map_list = []
    with open(get_full_path(path)) as data_map:
        level_data = reader(data_map)
        for row in level_data:
            level_map_list.append(list(row))
        # return a 2D list
        return level_map_list


def get_full_path(relative_path: str):
    """get th right path for pyinstaller to work properly"""
    relative_path = os.path.normpath(relative_path)
    if '.' not in relative_path:
        # if there is no point in the path it's just a folder, so I add \. Else it's a file.
        relative_path += '\\'
    if hasattr(sys, '_MEIPASS'):
        # if sys has a _MEIPASS attribute, the whole project is loaded from a single compiled executable
        # _MEIPASS is the temp path where files are extracted
        abs_path = sys._MEIPASS
    else:
        abs_path = os.path.abspath('..')
    return os.path.join(abs_path, relative_path)


def get_pos_from_id(tile_id: int):
    """calculate the position of the sprite on the spritesheet from an ID"""
    x = tile_id % 25        # modulo
    y = tile_id // 25       # reste de la division euclidienne
    return x, y


def load_character(character: str):
    """load an image of a given character from his name (and the const CHAR_LIST)
    return a image (type surf)"""
    assert character in settings.CHAR_LIST, f"{character} not in CHAR_LIST"
    loaded_character = (
        pygame.image.load(get_full_path(f'images/NinjaAdventure/Actor/Characters/{character}/SpriteSheet.png')).convert_alpha()
    )
    return loaded_character


def level_files_path(num: int):
    """return a list of path for a given level num"""

    # os.listdir only extract a list of files names from the directory
    list_of_files = os.listdir(get_full_path(f"level/{num}/"))

    # add level/{num}/ to every file
    for i, file in enumerate(list_of_files):
        list_of_files[i] = get_full_path(f"level/{num}/"+file)

    # list_of_file now contain a list of full path
    return list_of_files


def get_spritesheet(name: str, animated: bool):
    """return a spritesheet image"""

    if animated is True:
        path = get_full_path(f'images/NinjaAdventure/Backgrounds/Animated/{name}.png')
    else:
        path = get_full_path(f'images/NinjaAdventure/Backgrounds/Tilesets/{name}.png')
    spritesheeet = pygame.image.load(get_full_path(path)).convert_alpha()
    # return a image
    return spritesheeet


def render_text(text: str, size: int, color: tuple):
    """return a image from a text, a size and a color """
    # assertions
    assert len(color) == 3, f'expects 3, got {len(color)}'

    pygame.font.init()
    font = pygame.font.SysFont(pygame.font.get_default_font(), size)
    return font.render(text, True, color)
