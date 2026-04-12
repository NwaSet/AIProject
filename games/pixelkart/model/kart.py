from games.pixelkart.const import *
import random
from games.pixelkart.model.race import Race

class Kart:

    def __init__(
        self,
        id: int,
        name: str,
        game: object = None
    ):
        self.id = id
        self.name = name

        self.game = game

        self.nb_win = 0
        self.nb_lose = 0
        self.nb_tie = 0

        self.lap = 0

        self.coord = None
        self.color = "gray"
        self.speed = 0
        self.direction = "East"
    
    def play(self):
        """
        chose a random choice between all legal move given by the model.
        """
        actions = []

        actions.extend([-1,0,1])

        for direction in ACTION_TO_MOVE.keys():
            if self.game.is_legal_move(self.direction, direction):
                actions.append(direction)
        
        return random.choice(actions)

    def win(self) -> None :
        """
        add one win
        """

        self.nb_win += 1


    def lose(self) -> None :
        """
        add one lose
        """

        self.nb_lose += 1
    
    def tie(self) -> None :
        """
        add one tie
        """

        self.nb_tie += 1 
