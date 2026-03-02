from .gamesControlers import *
import tkinter as tk

class GameSelectionView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.view = self
        self.case1 = tk.Button(self, text="Mikado", command=lambda: self.controller.start_game("mikado"))
                               
        self.case1.pack(pady=10)

        self.case2 = tk.Button(self, text="cubee", command=lambda: self.controller.start_game("cubee"))
                               
        self.case2.pack(pady=10)

        self.case3 = tk.Button(self, text="kart", command=lambda: self.controller.start_game("kart"))
        self.case3.pack(pady=10)