from tkinter import *
from .settings_frame.settings_frame import settings

# python -m games.pixelkart.view.game_view

class View(Tk):
    def __init__(self, controler, *args, **kwargs) :
        super().__init__(*args, **kwargs)

        self.title('pixel kart')
        self.geometry('500x500')
        self.resizable(False, False)

        self.controler = controler
        
        # frame 1 == settings
        # frame 2 == game view
        self.next_frame = 1

        self.toggle()
    
    def show_settings(self) :
        setting = settings(self, self.controler)
        setting.pack()

    def show_game(self) :
        pass

    def toggle(self) :
        if self.next_frame == 1 :
            self.show_settings()
            self.next_frame = 2
        else :
            self.show_game()
            self.next_frame = 1

if __name__ == "__main__" :
    view = View(None)
    view.mainloop()