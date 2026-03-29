from games.mikado.player.player import *
from games.mikado.player.ai import *
from games.mikado.player.human import *
from games.mikado.controler.game_controler import *
from games.mikado.model.game_model import *
from games.mikado.view.view import *

from games.mikado.train import *


def start_mikado_Game() :
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
    # Print a comparison between the @ais
    names = f"{'':4}"
    stats1 = f"{'':4}"
    stats2 = f"{'':4}"

    for ai in ais :
        names += f"{ai.name:^15}"
        stats1 += f"{str(ai.nb_win)+'/'+str(ai.nb_game):^15}"
        stats2 += f"{f'{ai.nb_win/ai.nb_game*100:4.4}'+'%':^15}"

    print(names)
    print(stats1)
    print(stats2)
    print(f"{'-'*4}{'-'*len(ais)*15}")

    all_v_dict = {key : [ai.v_fuction.get(key,0.0) for ai in ais] for key in ais[0].v_fuction.keys()}
    sorted_v = lambda v_dict : sorted(filter(lambda x : type(x[0])==int ,v_dict.items()))
    for state, values in sorted_v(all_v_dict):
        print(f"{state:2} :", end='')
        for value in values:
            print(f"{value:^15.3}", end='')
        print()