import random

class GameModel :
    def __init__(self, grid_size, Player1, Player2):

        self.grid_size = grid_size
        self.grid[self.grid_size] = []

        self.player1 = Player1
        self.player2 = Player2

        self.player1.coord = (self.grid_size-1, self.grid_size-1)
        self.player2.coord = (0, 0)        

        self.score = {self.player1.__str__() : 0, self.player2.__str__() : 0}

        self.current_player = self.shuffle()
    
    def shuffle(self) :
        return random.choice(self.player1, self.player2)

    def switch_player(self) :
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2
    
    def reset(self) :
        self.grid[self.grid_size] = []
        self.current_player = self.shuffle()
        self.score = (0, 0)
        
        