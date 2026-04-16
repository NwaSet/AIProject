from games.pixelkart.model.kart import Kart

class Human(Kart):
    """
    Human kart used in a PixelKart race.
    """

    def __init__(
        self,
          id: int,
        name: str,
        color: str,
        game: object = None
    ) -> None:
        """
        Initialize a human player.

        Args:
            id (int): Unique identifier of the player.
            name (str): Name of the player.
            color (str): Color associated with the player (used in UI).
            game (GameModel, optional): Game instance the player belongs to.
        """

        super().__init__(id,name,game)

        self.color = color
