from .controler.controler import gameControler
from .model.cubee_model import GameModel
from .view.view import View
from .player.player import Player
from .player.human import Human
from .player.ai import Ia
from .dao.dao import Dao


def start_cubee_game():
    """
    function that permiet to launch the cubee game
    """

    train_ai()
    bot = Ia(2, "ia1", epsilon=0)
    flo = Human(1, "flo", "red")
    # yo = Human(2, "yo", "blue")
    ctrl = gameControler()
    game = GameModel(5, Player1=flo, Player2=bot, controler=ctrl)
    view = View(ctrl)
    ctrl.start_game()


def train_ai():
    ia1 = Ia(
            id=1,
            name="ia1",
            epsilon=1,
            lr=0.01,
            gamma=0.7,
        )

    ia2 = Ia(
            id=2,
            name="ia2",
            epsilon=1,
            lr=0.01,
            gamma=0.7,
        )

    game = GameModel(3, False,  ia1, ia2)

    for i in range(10_000):
        game.play()
        game.reset()
        print(i)
