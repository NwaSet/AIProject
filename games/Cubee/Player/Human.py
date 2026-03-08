from .Player import *
import keybord

class Human(Player):
    def __init__(self,name,color, game = None):
        super.__init__(name,game)
        
        self.color = color

    def play(self):
        return keybord.read_key()
        
