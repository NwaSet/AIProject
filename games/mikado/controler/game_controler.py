from games.mikado.player.player import *
from games.mikado.player.ai import *
from games.mikado.player.human import *
from games.mikado.model.game_model import *
from games.mikado.view.view import *

class GameController :

    """
    Controller layer of the Mikado game.

    Responsible for:
    - Coordinating interactions between the model and the view
    - Handling user and AI actions
    - Updating the view when the game state changes
    """

    def __init__(self) -> None :
        """
        Initialize the controller without linking model and view yet.
        """

        self.game = None
        self.view = None
    
        
    def get_nb_matches(self) -> int :
        """
        return the nb stick left in the game
        """

        return self.game.nb_stick
    

    def get_status_message(self) -> str :
        """
        return a str to say whose turn it is
        """

        return f"turn to {self.game.current_player} !"


    def get_loser(self) -> object :
        """
        return the loser
        """

        return self.game.loser


    def handle_human_move(
            self,
            nb_stick_taken : int
            ) -> None :
        """
        handle the move of a humain and if next player is an ai, call the handle_ai_move
        """

        if isinstance(self.game.current_player, Human) :
            self.game.step(nb_stick_taken)
            self.view.update_view() 

            if self.game.is_game_over() :
                self.handle_end_game()
            else :
                if not isinstance(self.game.current_player, Human) :
                    self.handle_ai_move()
    

    def handle_ai_move(self) -> None :
        """
        handle the move of an ai
        """

        nb_stick_taken = self.game.current_player.play()
        
        self.game.step(nb_stick_taken)
        
        self.view.update_view()

        if self.game.is_game_over():
            self.handle_end_game()
    

    def handle_end_game(self) -> None :
        """
        say to the view that game is over
        """

        self.view.end_game()
    

    def need_refresh(self) -> None :
        """
        ask the view to update the display
        """

        self.view.update_view()

    
    def start_game(self) -> None :
        """
        Start the graphical loop of the game
        """

        self.view.update_view()

        if not isinstance(self.game.current_player, Human):
            print(f"L'IA {self.game.current_player} commence !")
            self.handle_ai_move()

        self.view.mainloop()
    

    def reset_game(self) -> None :
        """
        Reset the game and reset the view
        """

        self.game.reset()
        self.view.reset()