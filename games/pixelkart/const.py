### PixelKart

PIXEL_TYPES = {
        "ROAD":{"color":"grey", "letter":"R"},
        "GRASS":{"color":"green", "letter":"G"},
        "WALL":{"color":"black", "letter":"W"},
        "FINISH":{"color":"yellow", "letter":"F"}
    }
ACTION_TO_MOVE = {
        "North": (-1, 0),
        "South": (1, 0),
        "West": (0, -1),
        "East": (0, 1),
    }

MOVE_TO_ACTION = {
        (-1, 0): "North",
        (1, 0): "South",
        (0, -1): "West",
        (0, 1): "East",

    }

SETTINGS_TO_ACTION = {
    "turn_right" : "turn_right",
    "turn_left" : "turn_left",
    "accelerate" : 1,
    "decelerate" : -1,
    "pass_turn" : "pass_turn"
}

NORTH_TO_MOVE = {
    "turn_right" : "East",
    "turn_left" : "West"
}

SOUTH_TO_MOVE = {
    "turn_right" : "West",
    "turn_left" : "East"
}

EAST_TO_MOVE = {
    "turn_right" : "South",
    "turn_left" : "North"
}

WEST_TO_MOVE = {
    "turn_right" : "North",
    "turn_left" : "South"
}
