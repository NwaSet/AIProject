from .player import *
from .gameControler import *
from .gameModel import *
from .view import *

from .train import training, compare_ai

def start_mikado_Game() :
    """
    create fiew Ai, train them then play aginst one
    
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

    training(Bob, Alice,  1_000_000, 10_000)
    training(Randy, Basic, 100_000, 10_000)
    compare_ai(Bob, Alice, Randy)
    Bob.upload()

    Bob.download("Bob")

    florian = Human("flo")
    game_controler = GameController()
    game_view = GameView(game_controler)
    game = GameModel(florian,Bob, game_controler)
    game_controler.start_game()