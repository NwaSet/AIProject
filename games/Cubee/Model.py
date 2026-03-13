import random

class GameModel :
    def __init__(self, grid_size, Player1=None, Player2=None):

        self.grid_size = grid_size
        self.grid = []
        self.init_grid()

        self.player1 = Player1
        self.player2 = Player2

        self.player1.coord = (self.grid_size-1, self.grid_size-1)
        self.player2.coord = (0, 0)        

        self.score = {self.player1.__str__() : 0, self.player2.__str__() : 0}

        self.current_player = self.shuffle()
    
    def init_grid(self) :
        for _ in range(self.grid_size) :
            row = []
            for _ in range(self.grid_size) :
                row.append(0)
            self.grid.append(row)
        self.grid[0][0] = 2
        self.grid[self.grid_size-1][self.grid_size-1] = 1
    
    def shuffle(self) :
        return random.choice(self.player1, self.player2)

    def switch_player(self) :
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2
    
    def reset(self) :

        self.grid = []
        self.init_grid()

        self.player1.coord = (self.grid_size-1, self.grid_size-1)
        self.player2.coord = (0, 0) 

        self.current_player = self.shuffle()

        self.score = {self.player1.__str__() : 0, self.player2.__str__() : 0}
    
    def is_game_over(self) :
        """
        check if the all grid is complet
        return true if the all grid is used else false
        """
        return 0 not in self.grid

    def legal_move(self) :
        """
        verify all possible move for the player,
        return a list of tuple for all possible action == (x, y) .
        """
        player_coord_x, player_coord_y = self.current_player.coord

        possible_direction = [
            (0, 1)  # up
            (0, -1) # down
            (-1, 0) # left
            (1, 0)  # right
        ]

        legal_action = []

        for direction_x, direction_y in possible_direction :
            new_x = player_coord_x + direction_x
            new_y = player_coord_y + direction_y

            if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size :
                if self.grid[new_x][new_y] in (0, self.current_player.id):
                    legal_action.append((direction_x, direction_y))

    
    def step(self) :
        None
    
    def play(self) :
        None

    @property
    def winner(self) :
        None
    
    @property
    def loser(self) :
        None
