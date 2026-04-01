from .controler.controler import gameControler
from .model.cubee_model import GameModel
from .view.view import View
from .player.player import Player
from .player.human import Human
from .player.ai import Ia


def start_cubee_game():
    """
    function that permiet to launch the cubee game
    """

    # train_ai()
    bot = Ia(2, "ia1", epsilon=0)
    flo = Human(1, "flo", "red")
    # yo = Human(2, "yo", "blue")
    ctrl = gameControler()
    game = GameModel(5, Player1=flo, Player2=bot, controler=ctrl)
    view = View(ctrl)
    ctrl.start_game()


def train_ai() :
    bot_1 = Ia(1,"ia1")
    bot_2 = Ia(2,"ia1")

    for i in range(100_000) :
        if i % 10 == 0 :
            bot_1.next_epsilon()
            bot_2.next_epsilon()
            
        

        print(i)
        game = GameModel(5,False, bot_1,bot_2)
        game.play()

    print(bot_1.nb_win)
    print(bot_2.nb_win)
