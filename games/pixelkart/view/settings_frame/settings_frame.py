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

        settings_player_1 = playerSelection(self.player_selection_1, 1)
        settings_player_2 = playerSelection(self.player_selection_2, 2)

        settings_player_1.pack(padx=25)
        settings_player_2.pack(padx=25)

        self.player_selection_1.pack(side="left")
        self.player_selection_2.pack(side="left")

        # -------------------------
        # FRAME CIRCUIT (EN DESSOUS)
        # -------------------------
        self.circuit_frame = Frame(self)
        self.circuit_frame.pack(pady=5)

        settings_circuit = circuitSelection(self.circuit_frame, self.controler)
        settings_circuit.pack()