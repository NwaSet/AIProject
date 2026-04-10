from tkinter import *
from .circuit_frame import CircuitRaceFrame
from .player_info_frame import PlayerInfo
from .player_move_frame import PlayerMove


class RaceView(Frame):
    def __init__(self, parent, controler):
        super().__init__(parent, bg="#bdc3c7")

        self.controler = controler

        # -------------------------
        # LEFT : circuit
        # -------------------------
        self.left_frame = Frame(self, bg="#95a5a6")
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.circuit_frame = CircuitRaceFrame(self.left_frame)
        self.circuit_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # -------------------------
        # RIGHT : players
        # -------------------------
        self.right_frame = Frame(self, bg="#dfe6e9", width=320)
        self.right_frame.pack(side="right", fill="y", padx=10, pady=10)
        self.right_frame.pack_propagate(False)

        self.current_player_label = Label(
            self.right_frame,
            text="Current player : ?",
            font=("Arial", 14, "bold"),
            bg="#dfe6e9"
        )
        self.current_player_label.pack(pady=(15, 20))

        self.players_frame = Frame(self.right_frame, bg="#dfe6e9")
        self.players_frame.pack(fill="both", expand=True)

        # colonne joueur 1
        self.player1_column = Frame(self.players_frame, bg="#dfe6e9")
        self.player1_column.pack(side="left", fill="both", expand=True, padx=5)

        self.player1_info = PlayerInfo(
            self.player1_column,
            1
        )
        self.player1_info.pack(fill="x", pady=(0, 10))

        self.player1_move = PlayerMove(
            self.player1_column,
            self.controler,
            bg_color="#aed6f1"
        )
        self.player1_move.pack(expand=True, fill="both")

        # colonne joueur 2
        self.player2_column = Frame(self.players_frame, bg="#dfe6e9")
        self.player2_column.pack(side="left", fill="both", expand=True, padx=5)

        self.player2_info = PlayerInfo(
            self.player2_column, 2
        )
        self.player2_info.pack(fill="x", pady=(0, 10))

        self.player2_move = PlayerMove(
            self.player2_column,
            self.controler,
            bg_color="#f5b7b1"
        )
        self.player2_move.pack(expand=True, fill="both")

    def refresh(self):
        """
        Refresh uniquement le plateau + affichage texte.
        DTO attendu depuis le controller :

        {
            "grid": "GGGG,GRRG,GGGG",
            "player1_pos": (row, col),
            "player2_pos": (row, col),
            "player1_name": "...",
            "player2_name": "...",
            "player1_speed": 0,
            "player2_speed": 0,
            "player1_laps": 0,
            "player2_laps": 0,
            "current_player": 1
        }
        """
        if not self.controler:
            return

        dto = self.controler.get_game_dto()

        self.circuit_frame.dto_to_grid(dto["grid"])

        karts = {
            dto["player1_pos"]: "blue",
            dto["player2_pos"]: "red"
        }
        self.circuit_frame.update_view(karts)

        self.current_player_label.config(
            text=f"Current player : {dto['current_player']}"
        )

        self.player1_info.update_info(
            dto["player1_name"],
            dto["player1_pos"],
            dto["player1_speed"],
            dto["player1_laps"]
        )

        self.player2_info.update_info(
            dto["player2_name"],
            dto["player2_pos"],
            dto["player2_speed"],
            dto["player2_laps"]
        )