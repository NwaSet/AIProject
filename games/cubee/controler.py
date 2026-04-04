from .model.human import Human


class gameControler:
    """
    Controller class for the cubee game

    This class is responsible for:
    - Handling player actions (human or AI)
    - Updating the view after each action
    - Checking game state (end of game, winner, etc.)
    - Acting as an interface between the model and the view
    """

    def __init__(self, game: object = None, view: object = None) -> None:
        """
        initiate the gameModel and the View of the class
        """

        self.game = game
        self.view = view

    def handle_ai_move(self) -> None:
        """
        only if current player is not human :

        handle the move made by an ai,
        ask view to update its self
        if game is over, call the handle_end_game
        """

        if not isinstance(self.game.current_player, Human):
            move = self.game.current_player.play()

            self.game.step(move)

            self.view.update_view()
            if self.game.is_game_over():
                self.handle_end_game()

    def handle_human_move(self, move: tuple) -> None:
        """
        only if current player is human :

        handle move of a human,
        ask view to update
        and handle end game if game is over
        """

        if isinstance(self.game.current_player, Human):
            self.game.step(move)

            self.view.update_view()
            if self.game.is_game_over():
                self.handle_end_game()

    def handle_end_game(self) -> None:
        """
        say to the view to show the game over screen
        """

        self.view.game_over()

    def get_legal_move(self) -> list[tuple]:
        """
        get all legal move for a player
        """

        legal_move = self.game.legal_move()
        return legal_move

    def get_winner(self) -> object:
        """
        get the winner of the game
        """

        winner = self.game.winner
        return winner

    def get_loser(self) -> object:
        """
        return the loer of the game
        """

        loser = self.game.loser
        return loser

    def get_model_data(self) -> dict:
        """
        ask to the model all data that the view need
        """

        model_data = self.game.get_model_data()
        return model_data

    def start_game(self) -> None:
        """
        start the game, if ai need to play first, handle his move
        and start the view
        """

        if not isinstance(self.game.current_player, Human):
            print(f"L'IA {self.game.current_player} commence !")
            self.handle_ai_move()

        self.view.run()

    def reset_game(self) -> None:
        """
        reset all data, in the view and in the model to restart a game
        handle a step if the current player is an ai
        """

        self.game.reset()
        if not isinstance(self.game.current_player, Human):
            move = self.game.current_player.play()
            self.game.step(move)

        self.view.update_view()
