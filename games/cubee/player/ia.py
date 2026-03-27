from .player import Player


class IA(Player):
    def __init__(self, id: int, name: str, game: object = None) -> None:
        super().__init__(id, name, game)
        self.color = "gray"
