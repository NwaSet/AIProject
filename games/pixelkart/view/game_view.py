from tkinter import *
from .settings_frame.settings_frame import settings
from .game_frame.race_view import RaceView

# python -m games.pixelkart.view.game_view


class View(Tk):
    def __init__(self, controler, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title('pixel kart')
        self.geometry('1000x600')
        self.resizable(False, False)

        self.controler = controler

        # frame 1 == settings
        # frame 2 == game view
        self.next_frame = 1
        self.current_frame = None

        self.toggle()

    def show_settings(self):
        self.current_frame = settings(self, self.controler)
        self.current_frame.pack(fill="both", expand=True)

    def show_game(self):
        self.current_frame = RaceView(self, self.controler)
        self.current_frame.pack(fill="both", expand=True)
        self.current_frame.refresh()

    def toggle(self):
        if self.current_frame is not None:
            self.current_frame.destroy()

        if self.next_frame == 1:
            self.show_settings()
            self.next_frame = 2
        else:
            self.show_game()
            self.next_frame = 1


if __name__ == "__main__":
    view = View(None)
    view.mainloop()