from tkinter import *
from .settings_frame.settings_frame import settings
from .game_frame.race_view import RaceView

# python -m games.pixelkart.view.game_view


class View(Tk):
    """
    Root window of the PixelKart interface.
    """

    def __init__(self, controler: object, *args: object, **kwargs: object) -> None:
        """
        Initialize the root view and show the first frame.
        """
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

    def show_settings(self) -> None:
        """
        Display the settings frame.
        """
        self.current_frame = settings(self, self.controler)
        self.current_frame.pack(fill="both", expand=True)

    def show_game(self) -> None:
        """
        Display the race frame.
        """
        self.current_frame = RaceView(self, self.controler)
        self.current_frame.pack(fill="both", expand=True)
        self.current_frame.refresh()

    def toggle(self) -> None:
        """
        Switch between the settings frame and the game frame.
        """
        if self.current_frame is not None:
            self.current_frame.destroy()

        if self.next_frame == 1:
            self.show_settings()
            self.next_frame = 2
        else:
            self.show_game()
            self.next_frame = 1
    
    def refresh(self) -> None :
        """
        Refresh the current frame.
        """
        self.current_frame.refresh()


if __name__ == "__main__":
    view = View(None)
    view.mainloop()
