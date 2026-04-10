from tkinter import *

class circuitSelection(Frame) :

    def __init__(self, parent) :

        super().__init__(parent)

        self.label = Label(self, font="Arial 20", text="Circuit Selection.")

        self.circuit_editor = Button(self, self, text="Open Circuit Editor", width=10, command = lambda : self.controler.open) ### la commande ############