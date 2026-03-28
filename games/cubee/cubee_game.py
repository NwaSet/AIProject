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

    # flo = Human(1, "flo", "red")
    # yo = Human(2, "yo", "blue")
    # ctrl = gameControler()
    # game = GameModel(5, Player1=flo, Player2=yo, controler=ctrl)
    # view = View(ctrl)
    # ctrl.start_game()

    train_ai()

def train_ai() :
    bot_1 = IA(1,"ia1")
    bot_2 = IA(2,"ia1")

    for _ in range(100) :
        game = GameModel(3,False, bot_1,bot_2)
        game.play()
        
    print(bot_1.nb_win)
    print(bot_2.nb_win)
