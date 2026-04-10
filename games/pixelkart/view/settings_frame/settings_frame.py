from tkinter import *
from .player_selection_frame import playerSelection

class settings(Frame) :

    def __init__(self, parent, controler) :

        super().__init__(parent)

        self.controler = controler

        self.player_selection_1 = Frame(self)
        self.player_selection_2 = Frame(self)


        settings_player_1 = playerSelection(self.player_selection_1, 1)
        settings_player_2 = playerSelection(self.player_selection_2, 2)

        settings_player_1.pack(side="left", padx=25)
        settings_player_2.pack(side="left", padx=25)

        self.player_selection_1.pack(side="left")
        self.player_selection_2.pack(side="left")

        