from .player import *
from .gameControler import *
from .gameModel import *
from .view import *

def start_mikado_Game() :
    """
    
    Initialise  two player
                the game controller
                the Game view
                the game
    Start the game
    """
    player1 = Human("Yohann")
    player2 = Player("Ai")
        
    game_controler = GameController()
    game_view = GameView(game_controler)
    game = GameModel(player1,player2, game_controler)
    game_controler.start_game()