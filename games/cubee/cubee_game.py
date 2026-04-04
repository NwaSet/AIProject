from .controler import gameControler
from .model.cubee_model import GameModel
from .view import View
from .model.player import Player
from .model.human import Human
from .model.ai import Ia
from .dao.dao import Dao
from .train import *


def start_cubee_game():
    """
    function that permiet to launch the cubee game
    """

    flo = Human(1, "flo", "red")
    yo = Human(2, "yo", "blue")
    ctrl = gameControler()
    game = GameModel(5, Player1=flo, Player2=yo, controler=ctrl)
    view = View(ctrl)
    ctrl.start_game()
