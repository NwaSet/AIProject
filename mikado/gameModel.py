from .player import *
from .gameControler import *
from .gameModel import *
import random
import time

class GameModel :
    """
    GameModel for a Mikado game.

    Responsibilities:
    - Implement and enforce the game rules.
    - Track the number of games played and the wins/losses for each player.
    - Control and validate player actions during the game.
    """

    def __init__(self, player1: object, player2: object, controler: object , nb_stick: int = 12, displayable: bool =True) -> None :
        """
    Initialize a new GameModel instance.

        Args:
            player1 (object): The first player participating in the game.
            player2 (object): The second player participating in the game.
            controler (object): The controller responsible for handling game flow
                and triggering AI actions when needed.
            nb_stick (int, optional): The initial number of sticks at the start
                of the game. Defaults to 12.
            displayable (bool, optional): Indicates whether the game state should
                be displayed (e.g., in a GUI). Defaults to True.
        """
        self.original_nb_stick = nb_stick
        self.nb_stick = nb_stick

        self.controler = controler
        if self.controler is not None :
            self.controler.game = self
        
        self.player1 = player1
        self.player2 = player2
        
        self.displayable = displayable
        
        self.player1.game = self
        self.player2.game = self
        
        self.current_player = player1
        
        self.shuffle()

        if self.displayable :
            if not isinstance(self.current_player, Human) :
                self.controler.handle_ai_move()
        
       
    def shuffle(self) -> None :
        """
        Changes the first player who play
        """
        players = [self.player1, self.player2]
        random.shuffle(players)
        self.current_player = players[0]
         
    def reset(self) -> None :
        """
        reset the game :
        - Put the number of stick in orginal number when the game restart
        - Call shuffle to change the first player
        """
        self.nb_stick = self.original_nb_stick
        self.shuffle()

        if self.displayable :
            if not isinstance(self.current_player, Human) :
                self.controler.handle_ai_move()
        
    def display(self) -> None :
        """
        Display the number of remaining sticks if the game is displayable.
        """
        if self.displayable :
            print(f"Allumettes restantes : {self.nb_stick}")
            

    def step(self, action: int) -> None :
        """
        Execute one turn of the game.

        This method:
        - Ensures the action does not exceed the remaining number of sticks.
        - Removes the specified number of sticks.
        - Checks if the game is over and updates players' statistics.
        - Switches the current player if the game continues.
        - Triggers AI move or refresh through the controller when necessary.

        Args:
            action (int): Number of sticks to remove (expected between 1 and 3).
        """

        if action > self.nb_stick:
            action = self.nb_stick

        self.nb_stick -= action

        if not self.is_game_over() :
            self.switch_player()

            if not isinstance(self.current_player, Human) :
                self.controler.need_refresh()
                self.controler.handle_ai_move()
            if not self.is_game_over() :
                self.controler.need_refresh()
        else :
            self.winner.win()
            self.loser.lose()
            self.controler.handle_end_game()


    def switch_player(self) -> None :
        """
        Change the current player
        """
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2
    
    def is_game_over(self) -> bool  :
        """
        Return if the game is over
        """
        return True if self.nb_stick <= 0 else False
    
    @property
    def get_current_player(self) -> object  :
        """
        Return the player whose turn it is.
        """
        return self.current_player
    
    @property
    def loser(self) -> object:
        """
        Return the loser
        """
        if self.is_game_over() :
            return self.current_player
    
    @property
    def winner(self) -> object :
        """
        Return the winner
        """
        if self.is_game_over() :
            return self.player1 if self.current_player == self.player2 else self.player2
        
    def play (self):
        self.reset()
        
        current_player = self.player1
        other_player = self.player2
        
        while self.nb_stick>0:
            self.display()
            
            self.nb_stick -= min(current_player.play(), self.nb_stick)
            
            current_player, other_player = other_player, current_player
            
        winner = current_player
        loser = other_player

        winner.win()
        loser.lose()
