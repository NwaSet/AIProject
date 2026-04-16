from games.pixelkart.view.game_view import View

from games.pixelkart.model.race import Race 
from games.pixelkart.model.human import Human
from games.pixelkart.model.kart import Kart
from games.pixelkart.model.circuit import Circuit

class pixelkartControler:


    def __init__(self) : 

        # will be created when view start the game. 
        self.game = None

        # init the view and start the mainloop.
        self.view = View(self)
        self.view.mainloop()
        
 
    def start_game(self, view_dto : dict) -> None :
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
        player_1_info = view_dto["player1"]
        player_2_info = view_dto["player2"]
        nb_laps = view_dto["nb_laps"]
        circuit_name = view_dto["circuit_name"]

        # create player 1
        if player_1_info["player_type"] == "ai" :
            player1 = Kart(player_1_info["player_number"], player_1_info["player_name"])
        elif player_1_info["player_type"] == "human" :
            player1 = Human(player_1_info["player_number"], player_1_info["player_name"], player_1_info["player_color"])

        # create player 2
        if player_2_info["player_type"] == "ai" :
            player2 = Kart(player_2_info["player_number"], player_2_info["player_name"])
        elif player_2_info["player_type"] == "human" :
            player2 = Human(player_2_info["player_number"], player_2_info["player_name"], player_2_info["player_color"])
        
        # create the circuit
        circuit = Circuit(circuit_name)

        # create the game and refresh view
        self.game = Race(circuit, nb_laps, True, player1, player2)

    def handle_human_move(self, move : str) -> None : 
        if isinstance(self.game.current_player, Human) :
            self.game.step(move)
            self.view.refresh()

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

    def refresh_view(self) -> None :
        self.view.refresh()

    def get_game_dto(self) -> None :
        """
        return the dto of the game.
        """
        return self.game.to_dto()

def start_pixelkart_game() :
    controler = pixelkartControler()
