from games.pixelkart.const import *
import random

class Kart:
    """
    Base kart class for a PixelKart player.
    """

    def __init__(
        self,
        id: int,
        name: str,
        game: object = None
    ) -> None:
        """
        Initialize a kart with its base race data.
        """
        self.id = id
        self.name = name

        self.game = game

        self.nb_win = 0
        self.nb_lose = 0
        self.nb_tie = 0

        self.lap = 0

        self.coord = None
        self.color = "Red"
        self.speed = 0
        self.direction = "East"
    
    def play(self) -> str:
        """
        chose a random choice between all legal move given by the model.
        """
        actions = ["pass_turn", "turn_left", "turn_right"]

        if self.speed < 2:
            actions.append("accelerate")
        if self.speed > -1:
            actions.append("decelerate")
        
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
