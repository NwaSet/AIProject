import random
from tkinter import *

class GameModel :
    def __init__(self, player1, player2, nb_stick=12, displayable =True) :
        self.original_nb_stick = nb_stick
        self.nb_stick = nb_stick
        
        self.player1 = player1
        self.player2 = player2
        
        self.displayable = displayable
        
        self.player1.game = self
        self.player2.game = self
        
        self.current_player = None
        
        self.shuffle()

        self.controler = None
        
       
    def shuffle(self) :
        players = [self.player1, self.player2]
        random.shuffle(players)
        self.current_player = players[0]
         
    def reset(self) :
        self.nb_stick = self.original_nb_stick
        self.shuffle()
        
    def display(self) :
        if self.displayable :
            print(f"Allumettes restantes : {self.nb_stick}")
            
    def step(self, action) :
        if (action < 1 or action > 3):
            return False

        if action > self.nb_stick:
            action = self.nb_stick

        self.nb_stick -= action
        return True

    def switch_player(self) :
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2

    def play (self) :
        self.reset
        
        while self.nb_stick>0 :
            self.display()
            
            self.step(self.current_player.play())
            
            self.switch_player()
        winner = self.get_winner
        print(winner.name)
    
    def is_game_over(self) :
        return self.nb_stick > 0
    
    @property
    def get_current_player(self) :
        return self.current_player
    
    @property
    def get_winner(self) :
        if self.is_game_over :
            return self.current_player
    
    @property
    def get_loser(self) :
        if self.is_game_over :
            return  self.player1 if self.current_player == self.player2 else self.player2
                  
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
    
    @property
    def nb_game(self: object) -> int :
        return self.nb_loose + self.nb_win
    
    def play(self, choice: int = None) -> int :
        if choice is None :
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

class GameView(Tk) :
    def __init__(self, controler = None):
        super().__init__()

        self.controler = controler

        self.title("Mikado Game")
        self.resizable(False, False)

        self.canvas = Canvas(self, width=700, height=200)
        self.canvas.pack()

        self.label_message = Label(self, text="oui oui", font="Arial 20")
        self.label_message.pack()

        self.button_frame = ButtonFrame(self, controler)
        self.button_frame.pack()


class ButtonFrame(Frame) :
    def __init__(self, parent, controler = None) :
        super().__init__(parent)

        self.controler = controler

        self.button1 = Button(self, text="take 1", width=10)
        self.button2 = Button(self, text="take 2", width=10)
        self.button3 = Button(self, text="take 3", width=10)

        self.button1.pack(side="left", pady=25, padx = 25)
        self.button2.pack(side="left",pady=25, padx = 25)
        self.button3.pack(side="left",pady=25, padx = 25)

    
class GamerController :
    None

if __name__ == "__main__" :
    player1 = Human("yo")
    player2 = Player("flo")
    
    # game = GameModel(player1,player2)
    # game.play()

    game_view = GameView()
    game_view.mainloop()
