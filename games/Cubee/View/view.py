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
