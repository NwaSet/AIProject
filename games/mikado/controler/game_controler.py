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
        Gère le coup de l'humain et lance celui de l'IA juste après.
        """
        # 1. Vérifie que c'est bien au tour de l'humain
        if isinstance(self.game.current_player, Human):
            self.game.step(nb_stick_taken)
            self.view.update_view() # On rafraîchit pour voir le coup de l'humain

            # 2. Vérifie si l'humain a perdu
            if self.game.is_game_over():
                self.handle_end_game()
            else:
                # 3. SI LE JOUEUR SUIVANT N'EST PAS HUMAIN -> L'IA joue
                if not isinstance(self.game.current_player, Human):
                    # On appelle la méthode de l'IA
                    self.handle_ai_move()
    
    def handle_ai_move(self) -> None :
        """
        Fait jouer l'IA et met à jour la vue.
        """
        # L'IA (ou le Player random) décide combien il prend
        nb_stick_taken = self.game.current_player.play()
        
        # Le modèle met à jour le nombre d'allumettes
        self.game.step(nb_stick_taken)
        
        # On rafraîchit la vue pour montrer les allumettes enlevées par l'IA
        self.view.update_view()

        # On vérifie si l'IA a perdu
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

    # ============================================
    # Lifecycle
    # ============================================
    
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
