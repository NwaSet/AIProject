import random


class Player :

    """
    Represent a generic player in the game.

    This is a base class used for both human and AI players (not created yet).
    """

    def __init__(
            self,
            id : int,
            name: str,
            game : object = None
            ) -> int :
        """
        Initialize a player.

        Args:
            id (int): Unique identifier of the player.
            name (str): Name of the player.
            game (GameModel, optional): Game instance the player belongs to.
        """

        self.name = name
        self.game = game

        self.nb_win = 0
        self.nb_lose = 0
        self.tie = 0
        self.coord = None
        self.color = "gray"

        self.id = id


    def play(self) -> tuple :
        """
        chose a random choice between all legal move given by the model.
        """

        return random.choice(self.game.legal_move())


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


    def __str__(self) -> str :
        return self.name
