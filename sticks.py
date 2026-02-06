import random
from tkinter import *

"""
modification :
    enlever l'init de interface, comme ca on commence par faire le link entre toutes les class
"""

class Game :
    def __init__(self, player1, player2, nb_stick=12, displayable =True):
        self.original_nb_stick = nb_stick
        self.nb_stick = nb_stick
        
        self.player1 = player1
        self.player2 = player2
        
        self.displayable = displayable
        
        self.player1.game = self
        self.player2.game = self
        
        self.shuffle()
        
       
    def shuffle(self):
        players = [self.player1, self.player2]
        random.shuffle(players)
        self.player1, self.player2 = players
         
    def reset(self):
        self.nb_stick = self.original_nb_stick
        self.shuffle()
        
    def display(self):
        if self.displayable:
            print(f"Allumettes restantes : {self.nb_stick}")
            
    def step(self, action):
        if (action < 1 or action > 3):
            return False

        if action > self.nb_stick:
            action = self.nb_stick

        self.nb_stick -= action
        return True

    def play (self):
        self.reset
        
        current_player = self.player1
        other_player = self.player2
        
        while self.nb>0:
            self.display()
            
            self.step(current_player.play())
            
            current_player, other_player = other_player, current_player
            
        winner = current_player
        loser = other_player

        winner.win()
        loser.loose()
                  
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
    def nb_game(self: object) -> int:
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
        choice = int(input("how many sticks do you wan't to take (1 - 3): "))
        return choice

class Ai(Player) :
    None

class Interface :
    def __init__(self, controler):

        self.controler = controler

        self.root = Tk()
        self.root.title("Mikado Game")
        self.root.geometry("850x450")
        self.root.resizable(False, False)

        self.canvas = Canvas(self.root, width= 800, height=300)
        self.canvas.pack()

        self.root.mainloop()

    
    def set_controler(self, controler) :
        self.controler = controler
    
    def show_stick(self, x_pos) :
        self.canvas.create_rectangle(x_pos, 100, x_pos+5, 250, fill="brown")
    
    def init_stick(self) :
        nb_stick = self.controler.get_nb_stick()
        for i in range(nb_stick) :
            self.show_stick(i*10)

class Controler :
    def __init__(self, game, interface):
        self.game = game
        self.interface = interface
    
    def get_nb_stick(self) :
        return self.game.nb_stick


if __name__ == "__main__":
    player1 = Human("yo")
    player2 = Player("flo")
    
    controler = Controler()
    game = Game(player1,player2)
    gui = Interface(controler)
