from tkinter import *


class PlayerMove(Frame):
    """
    Display the action buttons for one player.
    """

    def __init__(
        self,
        parent: object,
        controler: object,
        bg_color: str = "#ecf0f1",
    ) -> None:
        """
        Initialize the move panel and its buttons.
        """
        super().__init__(parent, bg=bg_color, bd=1, relief="solid")

        self.controler = controler
        self.bg_color = bg_color

        self.title_label = Label(
            self,
            text="Actions",
            font=("Arial", 12, "bold"),
            bg=bg_color
        )
        self.title_label.pack(pady=(10, 5))

        self.accelerate_button = Button(
            self,
            text="Accelerate",
            width=15,
            command=self.on_accelerate
        )
        self.accelerate_button.pack(pady=10)

        self.decelerate_button = Button(
            self,
            text="Deccelerate",
            width=15,
            command=self.on_decelerate
        )
        self.decelerate_button.pack(pady=10)

        self.turn_left_button = Button(
            self,
            text="Turn left",
            width=15,
            command=self.on_turn_left
        )
        self.turn_left_button.pack(pady=10)

        self.turn_right_button = Button(
            self,
            text="Turn right",
            width=15,
            command=self.on_turn_right
        )
        self.turn_right_button.pack(pady=10)

        self.on_pass_button = Button(
            self,
            text="Pass turn",
            width=15,
            command=self.on_pass
        )
        self.on_pass_button.pack(side="bottom", pady=15)

    def on_accelerate(self) -> None:
        """
        Trigger the accelerate action.
        """
        if self.controler:
            self.controler.accelerate()

    def on_decelerate(self) -> None:
        """
        Trigger the decelerate action.
        """
        if self.controler:
            self.controler.decelerate()

    def on_turn_left(self) -> None:
        """
        Trigger the turn-left action.
        """
        if self.controler:
            self.controler.turn_left()

    def on_turn_right(self) -> None:
        """
        Trigger the turn-right action.
        """
        if self.controler:
            self.controler.turn_right()

    def on_pass(self) -> None:
        """
        Trigger the pass action.
        """
        if self.controler:
            self.controler.pass_turn()
