import random

class Player:
    def __init__(self,id,  name: str, game= None):
        self.name = name
        self.game = game

        self.nb_win = 0
        self.nb_lose = 0
        self.tie = 0
        self.coord = None
        self.color = "gray"

        self.id = id

    def play(self):
        return random(self.game.legal_move())

    def win(self):
        self.nb_win += 1

    def lose(self):
        self.nb_lose += 1

    def __str__(self):
        return self.name
