from .Player import *


class Human(Player):
    def __init__(self, id, name, color, game=None):
        super().__init__(id, name, game)

        self.color = color
