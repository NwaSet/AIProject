import tkinter as tk
# from Cubee import Model


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

        self.canva = tk.Canvas(
            self.root,
            width=self.size * self.nb_case + 200,
            height=self.size * self.nb_case,
        )
        self.canva.pack(padx=(20, 5))
        self.cases = []

    def creation_grid(self):

        for row in range(self.nb_case):
            line = []
            for col in range(self.nb_case):
                x = col * self.size
                y = row * self.size

                case = self.canva.create_rectangle(
                    x,
                    y,
                    x + self.size + 2,
                    y + self.size + 2,
                    outline="gray",
                    width=2,
                )

                line.append(case)

            self.cases.append(line)

    def creation_score(self):
        self.score_text = self.canva.create_text(
            self.nb_case * self.size + 50,
            20,
            text=f"Score: \n player1 : {self.score}",
        )

    def update_score(self, new_score):
        self.score = new_score
        self.canva.itemconfig(self.score_text, text=f"Score: {self.score}")

    def run(self):
        self.creation_grid()
        self.creation_score()
        self.root.mainloop()


if __name__ == "__main__":
    view = View()
    view.run()