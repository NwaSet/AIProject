import random


class Player :
    """
    A class represent a player

    Attributs:
        name (str)  : Player name
        game (Game) : Player game where he can be playing, he is not obliged to be in a game. 
    """
    def __init__(self, name: str, game: object = None) -> None :
        """
        Generic variable of a Player in the Mikado Game
        
        name(str):name of the player
        game(GameModel): game where play the player
        nb_win(int): total number of game won
        nb_lose(int): total number of game lose 
        """
        self.name = name
        self.game = game
        self.nb_win = 0
        self.nb_lose = 0
    
    def __str__(self) -> str:
        return self.name
    
    @property
    def nb_game(self: object) -> int :
        """
        Calculate the total of game played by the player
        
        Returns:
        int: the sum of the lose and the win
        """
        return self.nb_lose + self.nb_win
    
    def play(self) -> int :
        """ 
        Define th move logic
        
        returns:
            int: Random number between 1 and 3
        """
        return random.randint(1,3)
       
    def win(self) -> None :
        """
        Add a win to its total
        """
        self.nb_win += 1

    def lose(self) -> None :
        """
        Add a lose to its total
        """
        self.nb_lose += 1
        
class Human(Player) :
    None

class Ai(Player) :
    None
