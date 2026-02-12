from .player import *
from .gameModel import *
from .view import *

class GameController :
    def __init__(self):
        self.game = None
        self.view = None
    
    def get_nb_matches(self) :
        return self.game.nb_stick
    
    def get_status_message(self) :
        return f"turn to {self.game.current_player} !"

    def get_loser(self) :
        return self.game.loser
    
    def handle_human_move(self, nb_stick_taken) :
        if isinstance(self.game.current_player, Human):
            self.game.step(nb_stick_taken)
    
    def handle_ai_move(self) :
        nb_stick_taken =self.game.current_player.play()
        self.game.step(nb_stick_taken)
    
    def handle_end_game(self) :
        self.view.end_game()
    
    def need_refresh(self) :
        self.view.update_view()
    
    def start_game(self) :
        self.view.update_view()
        self.view.mainloop()
    
    def reset_game(self) :
        self.game.reset()
        self.view.reset()
