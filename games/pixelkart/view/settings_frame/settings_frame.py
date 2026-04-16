from tkinter import *
from .player_selection_frame import playerSelection
from .circuit_selection_frame import circuitSelection


class settings(Frame):
    """
    Settings view used to prepare a new race.
    """

    def __init__(self, parent: object, controler: object) -> None:
        """
        Initialize the player and circuit settings widgets.
        """
        super().__init__(parent, bg="#ecf0f1")

        self.controler = controler

        # -------------------------
        # FRAME POUR LES JOUEURS
        # -------------------------
        self.players_box = Frame(self, bg="#d6ecff", bd=2, relief="groove")
        self.players_box.pack(padx=10, pady=5)

        self.players_frame = Frame(self.players_box, bg="#d6ecff")
        self.players_frame.pack(padx=2, pady=2)

        self.player_selection_1 = Frame(self.players_frame, bg="#d6ecff")
        self.player_selection_2 = Frame(self.players_frame, bg="#d6ecff")

        self.settings_player_1 = playerSelection(self.player_selection_1, 1)
        self.settings_player_2 = playerSelection(self.player_selection_2, 2)

        self.settings_player_1.pack(padx=8, pady=2)
        self.settings_player_2.pack(padx=8, pady=2)

        self.player_selection_1.pack(side="left", padx=2, pady=2)
        self.player_selection_2.pack(side="left", padx=2, pady=2)

        # -------------------------
        # FRAME CIRCUIT (EN DESSOUS)
        # -------------------------
        self.circuit_box = Frame(self, bg="#d4f5d0", bd=2, relief="groove")
        self.circuit_box.pack(padx=10, pady=2)

        self.circuit_frame = Frame(self.circuit_box, bg="#d4f5d0")
        self.circuit_frame.pack(padx=2, pady=2)

        self.settings_circuit = circuitSelection(self.circuit_frame, self.controler)
        self.settings_circuit.pack(padx=2, pady=2)

        self.start_button = Button(
            self,
            text="Start game",
            width=25,
            height=10,
            background="lightgray",
            command=self.start_game
        )
        self.start_button.pack(side="bottom", pady=25)

    def start_game(self) -> None:
        """
        Build the game DTO and start a new race.
        """
        player1_dto = self.settings_player_1.get_dto()
        player2_dto = self.settings_player_2.get_dto()
        circuit_name = self.settings_circuit.get_selected_circuit()
        nb_laps = self.settings_circuit.get_number_of_laps()

        game_dto = {
            "player1": player1_dto,
            "player2": player2_dto,
            "circuit_name": circuit_name,
            "nb_laps": nb_laps
        }

        if self.controler:
            self.controler.start_game(game_dto)
        self.master.toggle()
        
