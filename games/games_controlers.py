from games.mikado.mikado_game import *
from games.cubee.cubee_game import *


class GameSelectionController:
    """
    class that permit to choose the game we wan't to play
    """

    def start_game(
            self,
            game_name : str,
            view : object = None
            ) -> None :
        """
        start the choosen game
        """
        
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

