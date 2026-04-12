from tkinter import *


class PlayerMove(Frame):
    def __init__(self, parent, controler, bg_color="#ecf0f1"):
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

    def on_accelerate(self):
        if self.controler:
            self.controler.accelerate()

    def on_decelerate(self):
        if self.controler:
            self.controler.decelerate()

    def on_turn_left(self):
        if self.controler:
            self.controler.turn_left()

    def on_turn_right(self):
        if self.controler:
            self.controler.turn_right()

    def on_pass(self):
        if self.controler:
            self.controler.pass_turn()