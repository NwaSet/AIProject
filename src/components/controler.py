from components.interface import *
from core.game import *

class Controler :
    def __init__(self, game, interface):
        self.game = game
        self.gui = interface

        self.game.controler = self
        self.gui.controler = self

        self.gui.init_gui()
    
    def get_nb_stick(self) :
        return self.game.nb_stick
    
    def get_nb_unlit_stick(self) :
        return self.game.original_nb_stick - self.game.nb_stick
    
    def get_current_player(self):
        return self.game.player1.name
    
    def get_nb_original_stick(self) :
        return self.game.original_nb_stick
    
    def press_1_stick(self) :
        self.game.step(1)
    
    def press_2_stick(self) :
        self.game.step(2)

    def press_3_stick(self) :
        self.game.step(3)

    def update_game(self) :
        self.gui.update_gui()
    
    def is_game_over(self, looser_name) :
        self.gui.show_game_over(looser_name)