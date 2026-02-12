import random

class Player :
    """
    A class represent a player

    Attributs:
        name (str)  : Player name
        game (Game) : Player game where he can be playing, he is not obliged to be in a game. 
    """
    def __init__(self, name, game=None) :
        self.name = name
        self.game = game
        self.nb_win = 0
        self.nb_loose = 0
    
    def __str__(self):
        return self.name
    
    @property
    def nb_game(self: object) -> int :
        return self.nb_loose + self.nb_win
    
    def play(self) -> int :
        return random.randint(1,3)
        
    def win(self) :
        self.nb_win += 1

    def lose(self) :
        self.nb_loose += 1
        
class Human(Player) :
    def play(self) :
        pass

class Ai(Player) :
    None
