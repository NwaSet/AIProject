from .player import *
from .gameControler import *
from .gameModel import *
from .view import *

def start_mikado_Game() :
    player1 = Human("Florian")
    player2 = Player("Yohann")
        
    game_controler = GameController()
    game_view = GameView(game_controler)
    game = GameModel(player1,player2, game_controler)
    game_controler.start_game()