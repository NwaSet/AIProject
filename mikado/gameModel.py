from .player import *
from .gameControler import *
from .gameModel import *
import random

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
            self.winner.win()
            self.loser.lose()
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
    def loser(self) :
        if self.is_game_over() :
            return self.current_player
    
    @property
    def winner(self) :
        if self.is_game_over() :
            return self.player1 if self.current_player == self.player2 else self.player2
