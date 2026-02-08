from components.controler import *
from tkinter import *

class Interface :
    def __init__(self, width = 800, height = 300):

        self.width = width
        self.height = height

        self.controler = None

        self.root = Tk()
        self.root.title("Mikado Game")
        self.root.geometry("850x450")
        self.root.resizable(False, False)

        self.canvas = Canvas(self.root, width = self.width, height = self.height)
        self.canvas.pack()

    def draw_stick(self, x_pos, stick_wood_color, stick_head_color) :
        self.canvas.create_rectangle(x_pos, 150, x_pos+5, 300, fill=stick_wood_color)
        self.canvas.create_oval(x_pos-2, 145, x_pos+7, 160, fill=stick_head_color)

    def draw_all_button(self) :
        button_1_stick = Button(self.root, text="1 stick", width=10, command=self.controler.press_1_stick)
        button_2_stick = Button(self.root, text="2 stick", width=10, command=self.controler.press_2_stick)
        button_3_stick = Button(self.root, text="3 stick", width=10, command=self.controler.press_3_stick)

        button_1_stick.pack(side="left", anchor="e", expand=True)
        button_2_stick.pack(side="left", anchor="center", expand=True)
        button_3_stick.pack(side="left", anchor="w", expand=True)

    def show_current_player(self) :
        player_name = self.controler.get_current_player()
        self.canvas.create_text(
            self.width // 2,
            50,
            text=f"turn to : {player_name} !",
            fill="black",
            font=("Arial", 24)
        )
    
    def show_nb_stick(self) :
        nb_stick = self.controler.get_nb_stick()
        self.canvas.create_text(
            self.width // 2,
            100,
            text=f"number of sticks left : {nb_stick} !",
            fill="black",
            font=("Arial", 18)
        )

    def init_gui(self) :
        nb_stick = self.controler.get_nb_stick()
        for i in range(nb_stick) :
            self.draw_stick((i*54) + 100, "brown", "red")
        
        self.show_current_player()
        self.show_nb_stick()
        
        self.draw_all_button()

        self.root.mainloop()
    
    def update_gui(self) :
        self.canvas.delete("all")

        nb_stick = self.controler.get_nb_stick()
        for i in range(self.controler.get_nb_original_stick()) :
            if i < nb_stick :
                self.draw_stick((i*54) + 100, "brown", "red")
            else :
                self.draw_stick((i*54) + 100, "gray", "gray")
        
        self.show_current_player()
        self.show_nb_stick()

    def show_game_over(self, looser_name) :
        self.canvas.delete("all")

        self.canvas.create_text(
            self.width // 2,
            self.height // 2,
            text=f"{looser_name} : you loose !",
            fill="red",
            font=("Arial", 72)
        )