### PixelKart

PIXEL_TYPES = {
        "ROAD":{"color":"grey", "letter":"R"},
        "GRASS":{"color":"green", "letter":"G"},
        "WALL":{"color":"black", "letter":"W"},
        "FINISH":{"color":"yellow", "letter":"F"}
    }
ACTION_TO_MOVE = {
        "North": (0, -1),
        "South": (0, 1),
        "West": (-1, 0),
        "East": (1, 0),
    }

MOVE_TO_ACTION = {
        (0, -1): "North",
        (0, 1): "South",
        (-1, 0): "West",
        (1, 0): "East",

    }