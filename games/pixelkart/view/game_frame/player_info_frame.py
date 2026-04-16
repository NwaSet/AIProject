from tkinter import *


class PlayerInfo(Frame):
    """
    Display basic information about one player.
    """

    def __init__(
        self,
        parent: object,
        player_id: int,
        bg_color: str = "#dfe6e9",
    ) -> None:
        """
        Initialize the player information panel.
        """
        super().__init__(parent, bg=bg_color, bd=1, relief="solid")

        self.player_id = player_id
        self.bg_color = bg_color

        self.title_label = Label(
            self,
            text=f"Player {player_id}",
            font=("Arial", 14, "bold"),
            bg=bg_color
        )
        self.title_label.pack(pady=(10, 5))

        self.name_label = Label(
            self,
            text="Name : ?",
            bg=bg_color
        )
        self.name_label.pack(pady=2)

        self.position_label = Label(
            self,
            text="Position : ?",
            bg=bg_color
        )
        self.position_label.pack(pady=2)

        self.speed_label = Label(
            self,
            text="Speed : ?",
            bg=bg_color
        )
        self.speed_label.pack(pady=2)

        self.laps_label = Label(
            self,
            text="Laps : ?",
            bg=bg_color
        )
        self.laps_label.pack(pady=(2, 10))

    def update_info(
        self,
        name: str,
        position: tuple[int, int],
        speed: int,
        laps: int,
    ) -> None:
        """
        Update the displayed player information.
        """
        self.name_label.config(text=f"Name : {name}")
        self.position_label.config(text=f"Position : {position}")
        self.speed_label.config(text=f"Speed : {speed}")
        self.laps_label.config(text=f"Laps : {laps}")
