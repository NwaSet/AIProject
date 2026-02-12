from tkinter import *
from .gameControler import *
from .gameModel import *

class GameView(Tk) :
    def __init__(self, controler):
        super().__init__()

        self.controler = controler
        self.controler.view = self

        self.title("Mikado Game")
        self.resizable(False, False)

        self.canvas = Canvas(self, width=700, height=200)
        self.canvas.pack()

        self.label_message = Label(self, font="Arial 20")
        self.label_message.pack()

        self.button_frame = None
        self.reset_button_frame = None

        self.add_button()

    def update_view(self) :
        self.canvas.delete("all")

        self.draw_matches(self.controler.get_nb_matches())

        status_message = self.controler.get_status_message()
        self.label_message.config(text=status_message)


    def add_button(self) :
        self.button_frame = ButtonFrame(self, self.controler)
        self.button_frame.pack()
    
    def add_reset_button(self) :
        self.reset_button_frame = ResetButtonFrame(self, self.controler)
        self.reset_button_frame.pack()

    def end_game(self) :
        self.button_frame.destroy()
        self.canvas.delete("all")
        self.label_message.config(text=f"game over. . . {self.controler.get_loser()} you loose !!")

        self.add_reset_button()


    def reset(self) :
        self.update_view()
        self.reset_button_frame.destroy()
        self.add_button()

    def draw_matches(self, nb_stick) :
        for i in range(nb_stick) :
            self.canvas.create_rectangle((i*50)+73, 50 , (i*50)+77 , 150 , fill="brown")
            self.canvas.create_oval((i*50)+72, 43 , (i*50)+78 , 55 , fill="red")

    


class ButtonFrame(Frame) :
    def __init__(self, parent, controler) :
        super().__init__(parent)

        self.controler = controler

        self.button1 = Button(self, text="take 1", width=10,
                              command = lambda : self.controler.handle_human_move(1))
        self.button2 = Button(self, text="take 2", width=10,
                              command = lambda : self.controler.handle_human_move(2))
        self.button3 = Button(self, text="take 3", width=10,
                              command = lambda : self.controler.handle_human_move(3))

        self.button1.pack(side="left", pady=25, padx = 25)
        self.button2.pack(side="left",pady=25, padx = 25)
        self.button3.pack(side="left",pady=25, padx = 25)
    
class ResetButtonFrame(Frame) :
    def __init__(self, parent, controler) :
        super().__init__(parent)

        self.controler = controler

        self.reset_button = Button(self, text="Restart A New Game", width=30,
                                   command= lambda : self.controler.reset_game())
        self.reset_button.pack(pady=25)
