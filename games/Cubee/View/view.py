<<<<<<< HEAD
from tkinter import *
from Cubee import Model 

class View(Tk):
    def __init__(self, controler: object):
        super().__init__()

        self.title("Cubee")
        self.grid = Grid()
        self.controler = controler

    def display_grid(self):
        for i in range(controler.)
=======
import tkinter as tk
# from games.Cubee.model import Model


class View:
    def __init__(self):
        # self.controler = controler
        self.dic = {"player1": 2, "player2": 8}
        self.nb_case = 10
        self.size = 100
        self.score = 0
        self.score_text = "score"
        self.root = tk.Tk()
        self.root.title("Cubee")

        self.root.bind("<Left>", self.controler)

        self.root.bind("<Right>", self.controler)

        self.root.bind("<Up>", self.controler)

        self.root.bind("<Down>", self.controler)

        self.player_coord = ((0, 0), (9, 9))
        self.player_color = ("gray", "red")

        self.restart_button = tk.Button(
            self.root, text="Restart", command=self.update_view
        )
        self.owners = [[None for _ in range(self.nb_case)] for _ in range(self.nb_case)]
        self.max_size = self.size * self.nb_case
        self.canva = tk.Canvas(
            self.root,
            width=self.max_size + 200,
            height=self.max_size + 5,
        )
        self.canva.pack(padx=(20, 5))
        self.cases = []

    def creation_grid(self):
        self.canva.delete("all")
        offset = 4
        for row in range(self.nb_case):
            line = []
            for col in range(self.nb_case):
                x = col * self.size + offset
                y = row * self.size + offset

                case = self.canva.create_rectangle(
                    x,
                    y,
                    x + self.size + 2,
                    y + self.size + 2,
                    outline="gray",
                    width=2,
                    tags="grid",
                )

                line.append(case)

            self.cases.append(line)

        self.canva.create_rectangle(
            offset,
            offset,
            self.max_size + offset,
            self.max_size + offset,
            outline="gray",
            width=2,
        )

    def creation_score(self):
        self.score = 0
        self.score_text = self.canva.create_text(
            self.nb_case * self.size + 50,
            20,
            text=f"Score: \n player1 : {self.score}",
        )

    def update_score(self, new_score):
        self.score = new_score
        self.canva.itemconfig(self.score_text, text=f"Score: {self.score}")

    def game_over(self):
        self.canva.delete("grid")
        self.canva.create_text(
            self.size * self.nb_case / 2,
            self.size * self.nb_case / 2,
            text="Game Over",
            font=("Arial", 40, "bold"),
        )

        self.restart_button = tk.Button(
            self.root, text="Restart", command=self.update_view
        )

        self.canva.create_window(
            self.size * self.nb_case / 2,
            self.size * self.nb_case / 2 + 80,
            window=self.restart_button,
        )

    def display_player(self):

        self.canva.delete("player")

        radius = self.size // 3
        for i, (col, row) in enumerate(self.player_coord):
            x_center = col * self.size + self.size / 2
            y_center = row * self.size + self.size / 2

            x0 = x_center - radius
            y0 = y_center - radius
            x1 = x_center + radius
            y1 = y_center + radius

            self.canva.create_oval(
                x0,
                y0,
                x1,
                y1,
                fill=self.player_color[i],
                outline="black",
                width=2,
                tags="player",
            )
        for i, (col, row) in enumerate(self.player_coord):
            self.capture_case(i, col, row)

    def capture_case(self, player_index, col, row):
        self.owners[row][col] = player_index
        case_id = self.cases[row][col]
        self.canva.itemconfig(case_id, fill=self.player_color[player_index])

    def update_view(self):
        self.creation_grid()
        self.display_player()
        self.creation_score()
        self.root.mainloop()


if __name__ == "__main__":
    view = View()
    view.update_view()
>>>>>>> 39bfedad19760df8bd92adaa262d8bf43c7e0e35
