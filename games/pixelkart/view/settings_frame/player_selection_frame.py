from tkinter import *

POSSIBLE_PLAYER_COLOR = ["brown", "pink", "blue"]


class playerSelection(Frame):
    """
    Widget used to configure one player before the race.
    """

    def __init__(self, parent: object, player_number: int) -> None:
        """
        Initialize the player selection form.
        """
        super().__init__(parent, bg="#d6ecff", bd=1, relief="solid")

        bg = "#d6ecff"
        self.player_number = player_number

        self.label_player_number = Label(
            self,
            font="Arial 20",
            text=f"P{player_number}.",
            bg=bg
        )

        self.label_player_name = Label(
            self,
            font="Arial 14",
            text="Player name :",
            bg=bg
        )
        self.player_name = Text(self, height=1, width=20)

        self.player_type = StringVar(value="ai")
        self.label_player_type = Label(
            self,
            font="Arial 14",
            text="Player type :",
            bg=bg
        )
        self.player_type_sellection_1 = Radiobutton(
            self,
            text="IA",
            variable=self.player_type,
            value="ai",
            bg=bg,
            activebackground=bg
        )

        self.player_type_sellection_2 = Radiobutton(
            self,
            text="Human",
            variable=self.player_type,
            value="human",
            bg=bg,
            activebackground=bg
        )

        self.player_color = StringVar(value=POSSIBLE_PLAYER_COLOR[0])

        self.label_player_color = Label(
            self,
            font="Arial 14",
            text="Player color :",
            bg=bg
        )
        self.player_color_selection_1 = Radiobutton(
            self,
            text="brown",
            variable=self.player_color,
            value=POSSIBLE_PLAYER_COLOR[0],
            bg=bg,
            activebackground=bg
        )
        self.player_color_selection_2 = Radiobutton(
            self,
            text="pink",
            variable=self.player_color,
            value=POSSIBLE_PLAYER_COLOR[1],
            bg=bg,
            activebackground=bg
        )
        self.player_color_selection_3 = Radiobutton(
            self,
            text="blue",
            variable=self.player_color,
            value=POSSIBLE_PLAYER_COLOR[2],
            bg=bg,
            activebackground=bg
        )

        self.label_player_number.pack()
        self.label_player_name.pack()
        self.player_name.pack()

        self.label_player_type.pack()
        self.player_type_sellection_1.pack()
        self.player_type_sellection_2.pack()

        self.label_player_color.pack()
        self.player_color_selection_1.pack()
        self.player_color_selection_2.pack()
        self.player_color_selection_3.pack()

    def get_dto(self) -> dict[str, int | str]:
        """
        Return the configuration of the selected player.
        """
        return {
            "player_number": self.player_number,
            "player_name": self.player_name.get("1.0", "end-1c"),
            "player_type": self.player_type.get(),
            "player_color": self.player_color.get(),
        }
