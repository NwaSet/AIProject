import random 

class Game :
    None

class Player :
    """
    A class represent a player

    Attributs:
        name (str)  : Player name
        game (Game) : Player game where he can be playing, he is not obliged to be in a game. 
    """
    def __init__(self, name, game=None):
        self.name = name
        self.game = game
        self.nb_win = 0
        self.nb_loose = 0
    
    @property
    def nb_game(self) :
        """
        return : the number of game plaied by the player
        """
        return self.nb_loose + self.nb_win
    
    def play(self) :
        choice = random.randint(1,3)
        return choice

    def win(self) :
        self.nb_win += 1

    def loose(self) :
        self.nb_loose += 1
        

class Human(Player) :
    def play(self) :
        choice = input("how many sticks do you wan't to take (1 - 3): ")
        return choice

class Ai(Player) :
    None
