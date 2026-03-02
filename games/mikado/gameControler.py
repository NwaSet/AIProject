from .player import *
from .gameModel import *
from .view import *

class GameController :

    """
    Controller layer of the Mikado game.

    Responsible for:
    - Coordinating interactions between the model and the view
    - Handling user and AI actions
    - Updating the view when the game state changes
    """

    def __init__(self) -> None:
        """
        Initialize the controller without linking model and view yet.
        """
        self.game = None
        self.view = None
    
    # ============================================
    # Getters
    # ============================================
        
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

    def get_loser(self) -> object:
        """
        return the loser
        """
        return self.game.loser
    
    # ============================================
    # Gameplay
    # ============================================

    def handle_human_move(self, nb_stick_taken : int) -> None :
        """
        handle a move triggered by a human player
        
        :param nb_stick_taken: the number of stick the player take
        """
        if isinstance(self.game.current_player, Human):
            self.game.step(nb_stick_taken)
    
    def handle_ai_move(self) -> None :
        """
        handle a move triggered by an Ai
        """
        nb_stick_taken =self.game.current_player.play()
        self.game.step(nb_stick_taken)
    
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

    # ============================================
    # Lifecycle
    # ============================================
    
    def start_game(self) -> None :
        """
        Start the graphical loop of the game
        """
        self.view.update_view()
        self.view.mainloop()
    
    def reset_game(self) -> None :
        """
        Reset the game and reset the view
        """
        self.game.reset()
        self.view.reset()
