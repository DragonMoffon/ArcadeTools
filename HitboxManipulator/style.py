import json
from PIL import Image

import arcade

CHECKERBOARD = None
COLOURS = None
ALL_COLOURS = None


def hex_to_RGBA(_hex):
    if len(_hex) > 4:
        return tuple(int(_hex[i*2]+_hex[i*2+1], 16) for i in range(4))
    else:
        return tuple(int(_hex[i]+_hex[i], 16) for i in range(4))


def read_style(path):
    global COLOURS
    global ALL_COLOURS
    ALL_COLOURS = {}
    file = arcade.resources.resolve_resource_path(path)
    with open(file) as _file:
        data = json.load(_file)
        for theme in data['colours']:
            theme_colours = data['colours'][theme]
            ALL_COLOURS[theme] = {colour: hex_to_RGBA(theme_colours[colour]) for colour in theme_colours}

        COLOURS = ALL_COLOURS[data['default']]
