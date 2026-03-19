import random
from games.Cubee.model.Model.py import GameModel


class Player:
    def __init__(self, name: str, game: object = None):
        self.name = name
        self.game = game

        self.nb_win = 0
        self.nb_lose = 0
        self.tie = 0
        self.coord = None
<<<<<<< HEAD
=======
        self.color = "gray"
>>>>>>> 39bfedad19760df8bd92adaa262d8bf43c7e0e35

    def play(self):
        return random(self.game.legal_move())

    def win(self):
        self.nb_win += 1

    def lose(self):
        self.nb_lose += 1

    def __str__(self):
<<<<<<< HEAD
        return self.name
=======
        return self.name
>>>>>>> 39bfedad19760df8bd92adaa262d8bf43c7e0e35
