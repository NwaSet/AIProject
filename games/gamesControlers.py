from .mikado.mikadoGame import *
from .Cubee.cubeeGame import *

class GameSelectionController:
    """
    class that permit to choose the game we wan't to play
    """
    def start_game(self, game_name, view = None):
        if game_name == "mikado":
            print("Lancement Mikado")
            self.view.destroy()
            start_mikado_Game()
            
        elif game_name == "cubee":
            print("Lancement cubee")
            self.view.destroy()
            start_cubee_game()
            
        elif game_name == "pixelKart":
            print("Lancement pixelKart")
    