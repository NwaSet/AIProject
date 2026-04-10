from tkinter import *
from .player_selection_frame import playerSelection
from .circuit_selection_frame import circuitSelection


class settings(Frame):

    def __init__(self, parent, controler):
        super().__init__(parent)

        self.controler = controler

        # -------------------------
        # FRAME POUR LES JOUEURS
        # -------------------------
        self.players_frame = Frame(self)
        self.players_frame.pack(pady=20)

        self.player_selection_1 = Frame(self.players_frame)
        self.player_selection_2 = Frame(self.players_frame)

        self.settings_player_1 = playerSelection(self.player_selection_1, 1)
        self. settings_player_2 = playerSelection(self.player_selection_2, 2)

        self.settings_player_1.pack(padx=25)
        self.settings_player_2.pack(padx=25)

        self.player_selection_1.pack(side="left")
        self.player_selection_2.pack(side="left")

        # -------------------------
        # FRAME CIRCUIT (EN DESSOUS)
        # -------------------------
        self.circuit_frame = Frame(self)
        self.circuit_frame.pack(pady=5)

        self.settings_circuit = circuitSelection(self.circuit_frame, self.controler)
        self.settings_circuit.pack()
        
        self.start_button = Button (
            self,
            text= "Start gamme",
            width=25,
            command=self.start_game
        )
        self.start_button.pack(side="bottom", pady=25)
    
    def start_game(self):
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