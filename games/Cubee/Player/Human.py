from .Player import *


class Human(Player):
    def __init__(self, name, color, game=None):
        super.__init__(name, game)

        self.color = color
