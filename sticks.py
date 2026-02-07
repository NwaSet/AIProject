import random
from tkinter import *

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

        self.controler = None
        
       
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
    def __init__(self):

        self.controler = None

        self.root = Tk()
        self.root.title("Mikado Game")
        self.root.geometry("850x450")
        self.root.resizable(False, False)

        self.canvas = Canvas(self.root, width= 800, height=300)
        self.canvas.pack()

    def start_game(self) :
        self.root.mainloop()

    def draw_stick(self, x_pos) :
        self.canvas.create_rectangle(x_pos, 100, x_pos+5, 250, fill="brown")
        self.canvas.create_oval(x_pos-2, 95, x_pos+7, 110, fill="red")
        self.canvas.pack()

    def draw_all_stick(self) :
        nb_stick = self.controler.get_nb_stick()
        for i in range(nb_stick) :
            self.draw_stick((i*54) + 100)
    
    def draw_all_button(self) :
        button_1_stick = Button(self.root, text="1 stick", width=10) # add fonction
        button_2_stick = Button(self.root, text="2 stick", width=10) # add fonction
        button_3_stick = Button(self.root, text="3 stick", width=10) # add fonction

        button_1_stick.pack(side="left", anchor="e", expand=True)
        button_2_stick.pack(side="left", anchor="center", expand=True)
        button_3_stick.pack(side="left", anchor="w", expand=True)

class Controler :
    def __init__(self, game, interface):
        self.game = game
        self.gui = interface

        self.game.controler = self
        self.gui.controler = self

        self.gui.draw_all_stick()
        self.gui.draw_all_button()
        self.gui.start_game()
    
    def get_nb_stick(self) :
        return self.game.nb_stick


if __name__ == "__main__":
    player1 = Human("yo")
    player2 = Player("flo")
    
    game = Game(player1,player2)
    gui = Interface()
    controler = Controler(game, gui)
