from .gamesControlers import *
from tkinter import *

class GameSelectionView(Tk):
    """
    class that permit to display the view of the game selection
    """

    def __init__(self, controller : object) -> None:
        """
        init the view
        """
        super().__init__()


        self.controller = controller
        self.controller.view = self

        
        self.title("Game Center - Sélection")
        self.resizable(False, False)


        self.canvas = Canvas(self, width=500, height=150)
        self.canvas.pack()
        
        self.canvas.create_text(250, 75, text="CHOISISSEZ VOTRE JEU", 
                                fill="black", font=("Arial", 20, "bold"))

        self.selection_frame = None
        self.add_selection_buttons()

    def add_selection_buttons(self) -> None:
        """
        add and pack the button to choose the game
        """
        self.selection_frame = SelectionButtonsFrame(self, self.controller)
        self.selection_frame.pack(pady=20)


class SelectionButtonsFrame(Frame):
    """
    class that can create all button for all the possible choice.
    """

    def __init__(self, parent : object, controller : object) -> None:
        """
        init of the button class
        """
        super().__init__(parent)
        self.controller = controller


        self.btn_mikado = Button(self, text="Mikado", width=15, height=2,
                                 command=lambda: self.controller.start_game("mikado"))
        
        self.btn_cubee = Button(self, text="Cubee", width=15, height=2,
                                command=lambda: self.controller.start_game("cubee"))
        
        self.btn_kart = Button(self, text="Kart", width=15, height=2,
                               command=lambda: self.controller.start_game("pixelKart"))

        self.btn_mikado.pack(side="left", padx=10)
        self.btn_cubee.pack(side="left", padx=10)
        self.btn_kart.pack(side="left", padx=10)