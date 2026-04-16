from games.mikado.player.player import *
from games.mikado.player.ai import *
from games.mikado.player.human import *
from games.mikado.controler.game_controler import *
from games.mikado.model.game_model import *
from games.mikado.view.view import *

from games.mikado.train import *


def start_mikado_Game() -> None :
    """
    
    Initialise  two player
                the game controller
                the Game view
                the game
    Start the game
    """

    Basic = Player("Basic")
    Bob = AI("Bob")
    Alice = AI("Alice")
    Randy = AI("Randy")
    player1 = Human("yohann")

    training(Alice, Bob,  10000, 10)
    training(Randy, Basic, 10000, 10)
    Bob.nb_win = 0
    Bob.nb_lose = 0
    training(Bob, Basic, 10000, 10)
    compare_ai(Bob, Alice, Randy)
        
    game_controler = GameController()
    game_view = GameView(game_controler)
    game = GameModel(player1,Bob, game_controler)
    game_controler.start_game()
