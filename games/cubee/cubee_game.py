from .controler.controler import gameControler
from .model.cubee_model import GameModel
from .view.view import View
from .player.player import Player
from .player.human import Human


def start_cubee_game():
    """
    function that permiet to launch the cubee game
    """

    flo = Human(1, "flo", "red")
    yo = Human(2, "yo", "blue")

    ctrl = gameControler()

    game = GameModel(5, Player1=flo, Player2=yo, controler=ctrl)
    # print(game.grid)
    # ctrl.handle_human_move((1,0))
    # ctrl.handle_human_move((1,0))
    # print(game.grid)

    view = View(ctrl)
    ctrl.start_game()
