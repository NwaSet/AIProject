import random
from tkinter import *

class GameModel :
    def __init__(self, player1, player2, controler, nb_stick=12, displayable =True) :
        self.original_nb_stick = nb_stick
        self.nb_stick = nb_stick

        self.controler = controler
        self.controler.game = self
        
        self.player1 = player1
        self.player2 = player2
        
        self.dclisplayable = displayable
        
        self.player1.game = self
        self.player2.game = self
        
        self.current_player = player1
        
        self.shuffle()

        if not isinstance(self.current_player, Human) :
            self.controler.handle_ai_move()
        
       
    def shuffle(self) :
        players = [self.player1, self.player2]
        random.shuffle(players)
        self.current_player = players[0]
         
    def reset(self) :
        self.nb_stick = self.original_nb_stick
        self.shuffle()

        if not isinstance(self.current_player, Human) :
            self.controler.handle_ai_move()
        
    def display(self) :
        if self.displayable :
            print(f"Allumettes restantes : {self.nb_stick}")
            
    def step(self, action) :
        if (action < 1 or action > 3):
            return False

        if action > self.nb_stick:
            action = self.nb_stick

        self.nb_stick -= action

        if self.is_game_over() :
            self.controler.handle_end_game()
        else :
            self.switch_player()

            if not isinstance(self.current_player, Human) :
                self.controler.handle_ai_move()
            if not self.is_game_over() :
                self.controler.need_refresh()

        return True

    def switch_player(self) :
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2
    
    def is_game_over(self) :
        return True if self.nb_stick <= 0 else False
    
    @property
    def get_current_player(self) :
        return self.current_player
    
    @property
    def looser(self) :
        if self.is_game_over() :
            return self.current_player
    
    @property
    def winner(self) :
        if self.is_game_over() :
            return self.player1 if self.current_player == self.player2 else self.player2
 
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
    
    def __str__(self):
        return self.name
    
    @property
    def nb_game(self: object) -> int :
        return self.nb_loose + self.nb_win
    
    def play(self) -> int :
        return random.randint(1,3)
        
    def win(self) :
        self.nb_win += 1

    def loose(self) :
        self.nb_loose += 1
        
class Human(Player) :
    def play(self) :
        pass

class Ai(Player) :
    None

class GameView(Tk) :
    def __init__(self, controler):
        super().__init__()

        self.controler = controler
        self.controler.view = self

        self.title("Mikado Game")
        self.resizable(False, False)

        self.canvas = Canvas(self, width=700, height=200)
        self.canvas.pack()

        self.label_message = Label(self, font="Arial 20")
        self.label_message.pack()

        self.button_frame = None
        self.reset_button_frame = None

        self.add_button()

    def update_view(self) :
        self.canvas.delete("all")

        self.draw_matches(self.controler.get_nb_matches())

        status_message = self.controler.get_status_message()
        self.label_message.config(text=status_message)


    def add_button(self) :
        self.button_frame = ButtonFrame(self, self.controler)
        self.button_frame.pack()
    
    def add_reset_button(self) :
        self.reset_button_frame = ResetButtonFrame(self, self.controler)
        self.reset_button_frame.pack()

    def end_game(self) :
        self.button_frame.destroy()
        self.canvas.delete("all")
        self.label_message.config(text=f"game over. . . {self.controler.get_looser()} you loose !!")

        self.add_reset_button()


    def reset(self) :
        self.update_view()
        self.reset_button_frame.destroy()
        self.add_button()

    def draw_matches(self, nb_stick) :
        for i in range(nb_stick) :
            self.canvas.create_rectangle((i*50)+73, 50 , (i*50)+77 , 150 , fill="brown")
            self.canvas.create_oval((i*50)+72, 43 , (i*50)+78 , 55 , fill="red")

    


class ButtonFrame(Frame) :
    def __init__(self, parent, controler) :
        super().__init__(parent)

        self.controler = controler

        self.button1 = Button(self, text="take 1", width=10,
                              command = lambda : self.controler.handle_human_move(1))
        self.button2 = Button(self, text="take 2", width=10,
                              command = lambda : self.controler.handle_human_move(2))
        self.button3 = Button(self, text="take 3", width=10,
                              command = lambda : self.controler.handle_human_move(3))

        self.button1.pack(side="left", pady=25, padx = 25)
        self.button2.pack(side="left",pady=25, padx = 25)
        self.button3.pack(side="left",pady=25, padx = 25)
    
class ResetButtonFrame(Frame) :
    def __init__(self, parent, controler) :
        super().__init__(parent)

        self.controler = controler

        self.reset_button = Button(self, text="Restart A New Game", width=30,
                                   command= lambda : self.controler.reset_game())
        self.reset_button.pack(pady=25)


class GameController :
    def __init__(self):
        self.game = None
        self.view = None
    
    def get_nb_matches(self) :
        return self.game.nb_stick
    
    def get_status_message(self) :
        return f"turn to {self.game.current_player} !"

    def get_looser(self) :
        return self.game.looser
    
    def handle_human_move(self, nb_stick_taken) :
        if isinstance(self.game.current_player, Human):
            self.game.step(nb_stick_taken)
    
    def handle_ai_move(self) :
        nb_stick_taken =self.game.current_player.play()
        self.game.step(nb_stick_taken)
    
    def handle_end_game(self) :
        self.view.end_game()
    
    def need_refresh(self) :
        self.view.update_view()
    
    def start_game(self) :
        self.view.update_view()
        self.view.mainloop()
    
    def reset_game(self) :
        self.game.reset()
        self.view.reset()
            

if __name__ == "__main__" :
    player1 = Human("yo")
    player2 = Player("flo")
    
    game_controler = GameController()

    game_view = GameView(game_controler)

    game = GameModel(player1,player2, game_controler)

    game_controler.start_game()