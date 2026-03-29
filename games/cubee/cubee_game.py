from .controler.controler import gameControler
from .model.cubee_model import GameModel
from .view.view import View
from .player.player import Player
from .player.human import Human
from .player.ia import IA


def start_cubee_game():
    """
    function that permiet to launch the cubee game
    """

    train_ai()
    bot = IA(2, "ia1", epsilon=0)
    flo = Human(1, "flo", "red")
    # yo = Human(2, "yo", "blue")
    ctrl = gameControler()
    game = GameModel(3, Player1=flo, Player2=bot, controler=ctrl)
    view = View(ctrl)
    ctrl.start_game()


def train_ai() :

    for i in range(10_000) :
        x = 1
        if i % 1000 == 0 :
            x = max(0, x - 0.1)
        
        bot_1 = IA(1,"ia1", epsilon=x)
        bot_2 = IA(2,"ia1", epsilon=x)

        game = GameModel(3,False, bot_1,bot_2)
        game.play()

    print(bot_1.nb_win)
    print(bot_2.nb_win)
