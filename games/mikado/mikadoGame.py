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
    Basic = Player("Basic")
    Bob = AI("Bob")
    Alice = AI("Alice")
    Randy = AI("Randy")
    player1 = Player("yohann")

    training(Alice, Bob,  10000, 10)
    training(Randy, Basic, 10000, 10)
    Bob.nb_win = 0
    Bob.nb_lose = 0
    training(Bob, Basic, 10000, 10)
    compare_ai(Bob, Alice, Randy)
        
    game_controler = GameController()
    game_view = GameView(game_controler)
    game = GameModel(player1,Basic, game_controler)
    game_controler.start_game()

def training(ai1, ai2, nb_games , nb_epsilon):
    # Train the AIs @ai1 and @ai2 during @nb_games games
    # epsilon decrease every @nb_epsilon games
    training_game = GameModel(ai1, ai2, None,  12,  displayable = False)
    for i in range(0, nb_games):
        if i % nb_epsilon == 0:
            if type(ai1)==AI : ai1.next_epsilon()
            if type(ai2)==AI : ai2.next_epsilon()

        training_game.play()
        if type(ai1)==AI : ai1.train()
        if type(ai2)==AI : ai2.train()

        training_game.reset()

def compare_ai(*ais):
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