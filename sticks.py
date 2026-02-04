import random 

class Game :
    def __init__(self, nb, player1,player2,displayable:True):
        self.original_nb = nb
        self.nb = nb
        self.player1 = player1
        self.player2 = player2
        self.displayable = displayable
        self.shuffle()
        player1.game = self
        player2.game = self
        
    def shuffle(self):
        random.shuffle
         
    def reset(self):
        self.nb = self.original_nb
        shuffle()
    
    def step(self):

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
