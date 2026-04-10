from tkinter import *

class View(Tk):
    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)

        self.title('pixel kart')
        self.geometry('500x500')
        self.resizable(False, False)
        
        # frame 1 == settings
        # frame 2 == game view
        self.next_frame = 1
    
    def show_settings(self) :
        pass

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
    view = View()
    view.mainloop()