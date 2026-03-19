from ..Player.Human import Human

class gameControler:
    def __init__(self, game=None, view=None) -> None:
        self.game = game
        self.view = view

    def handle_ai_move(self) -> None:
        if not isinstance(self.game.current_player, Human):
            move = self.current_player.play()

            self.game.step(move)

            self.view.update_view()
            if self.game.is_game_over():
                self.handle_end_game()

    def handle_human_move(self, move: tuple) -> None:
        if isinstance(self.game.current_player, Human):
            self.game.step(move)

            self.view.update_view()
            if self.game.is_game_over():
                self.handle_end_game()

    def handle_end_game(self):
        self.view.game_over()

    def get_legal_move(self):
        legal_move = self.game.legal_move()
        return legal_move

    def get_winner(self):
        winner = self.game.winner
        return winner

    def get_loser(self):
        loser = self.game.loser
        return loser

    def get_model_data(self):
        model_data = self.game.get_model_data()
        return model_data

    def start_game(self):

        if not isinstance(self.game.current_player, Human):
            print(f"L'IA {self.game.current_player} commence !")
            self.handle_ai_move()
        
        self.view.run()

        

    def reset_game(self):
        self.game.reset()
        self.view.update_view()
