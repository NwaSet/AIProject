from games.Cubee.model.cubeeModel import GameModel
from games.Cubee.Player.Human import Human


class gameControler:
    def __init__(self, game=None, controler=None) -> None:
        self.game = game
        self.controler = controler

    def handle_ai_move(self) -> None:
        if not isinstance(self.game.current_player, Human):
            move = self.current_player.play()

            self.game.step(move)

            if self.game.is_game_over():
                self.handle_end_game()
            else:
                self.view.update_view()

    def handle_human_move(self, move: tuple) -> None:
        if isinstance(self.game.current_player, Human):
            self.game.step(move)

    def handle_end_game(self):
        self.view.end_game()

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

        self.view.update_view()

        if not isinstance(self.game.current_player, Human):
            print(f"L'IA {self.game.current_player} commence !")
            self.handle_ai_move()

        self.view.mainloop()

    def reset_game(self):
        self.game.reset()
        self.view.update_view()
