from components.controler import *
from components.player import *
from components.interface import *
from core.game import Game

if __name__ == "__main__":
    player1 = Human("yo")
    player2 = Human("flo")
    
    game = Game(player1,player2)
    gui = Interface()
    controler = Controler(game, gui)