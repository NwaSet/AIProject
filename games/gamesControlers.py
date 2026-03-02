from .mikado.mikadoGame import *

class GameSelectionController:
    def start_game(self, game_name, view = None):
        if game_name == "mikado":
            print("Lancement Mikado")
            self.view.destroy()
            start_mikado_Game()
            
            

        elif game_name == "cubee":
            print("Lancement cubee")
            

        elif game_name == "pixelKart":
            print("Lancement pixelKart")
    