import random

Class Player :
    def __init__(self,name: str, game: object = None):
        self.name = name
        self.game = game

        self.win = 0
        self.lose = 0
        self.tie = 0
        self.coord = None
        
    def play(self):
        return random(self.game.legal_move())

    def win(self):
        return self.win += 1

    def lose(self):
        return self.lose += 1
    
    def __str__(self):
        return slef.name
