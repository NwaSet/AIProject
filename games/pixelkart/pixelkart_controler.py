from .view.game_view import View

from .model.race import Race 
from .model.human import Human
from .model.kart import Kart

class pixelkart_controler:

    def __init__(self) : 

        self.view = View(self)

        # créer une game quand le view recoit le start game.
        self.game = None
    
    def start_game(view_dto : dict) -> None :
        """
        init a race and update the view.

        view_dto = {
            "player1": dict
            "player2": dict
            "circuit_name": str
            "nb_laps": int
        }

        player_dto = {
            "player_number": int
            "player_name": str
            "player_type": str
            "player_color": color
        }
        """
        pass

    def handle_human_move(self, move : str) -> None : 
        if isinstance(self.game.current_player, Kart) :
            self.game.step(move)
            self.view.refresh()
        if isinstance(self.game.current_player, Kart) :
            self.handle_ai_move()

    def handle_ai_move(self) -> None :
        if isinstance(self.game.current_player, Kart) :
            move = self.game.current_player.play()
            self.game.step(move)
        if isinstance(self.game.current_player, Kart) :
            self.handle_ai_move()

    def accelerate(self) -> None :
        self.handle_human_move("accelerate")

    def decelerate(self) -> None :
        self.handle_human_move("decelerate")

    def turn_left(self) -> None :
        self.handle_human_move("turn_left")

    def turn_right(self) -> None :
        self.handle_human_move("turn_right")

    def pass_turn(self) -> None :
        self.handle_human_move("pass_turn")

    def refresh_view(self) -> None : # possiblement retiré car me semble inutile
        self.view.refresh()

    def get_game_dto(self) -> None :
        """
        return the dto of the game.
        """
        return self.game.to_dto()