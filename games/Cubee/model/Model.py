import random
from Cubee.Player.Human import Human

class GameModel :

    possible_direction = [
            (0, 1),  # up
            (0, -1), # down
            (-1, 0), # left
            (1, 0)  # right
        ]
    
    def __init__(self, grid_size, display = True, Player1=None, Player2=None):

        self.grid_size = grid_size
        self.grid = []
        self.init_grid()

        self.display = display

        self.player1 = Player1
        self.player2 = Player2

        self.player1.coord = (self.grid_size-1, self.grid_size-1)
        self.player2.coord = (0, 0)        

        self.score = {self.player1.__str__() : 0, self.player2.__str__() : 0}

        self.current_player = self.shuffle()

        if display and not isinstance(self.current_player, Human) :
            self.step(self.current_player.play())

    
    def init_grid(self) :
        for _ in range(self.grid_size) :
            row = []
            for _ in range(self.grid_size) :
                row.append(0)
            self.grid.append(row)
        self.grid[0][0] = self.player2.id
        self.grid[self.grid_size-1][self.grid_size-1] = self.player1.id
    
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

        legal_action = []

        for direction_x, direction_y in GameModel.possible_direction :
            new_x = player_coord_x + direction_x
            new_y = player_coord_y + direction_y

            if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size :
                if self.grid[new_x][new_y] in (0, self.current_player.id):
                    legal_action.append((direction_x, direction_y))

        return legal_action
    
    def set_case(self) :
        p_x, p_y = self.current_player.coord
        self.grid[p_x][p_y] = self.current_player.id

    def step(self, move) :

        if move in self.legal_move() :
            self.current_player.coord += move
            self.set_case

        if self.is_game_over() :
            self.winner.win()
            self.loser.lose()
        else :
            self.switch_player()
            if not isinstance(self.current_player, Human) :
                self.step(self.current_player.play())
    
    def play(self) :
        
        while not self.is_game_over() :

            move = self.current_player.play()
            if move in self.legal_move() :
                self.current_player.coord += move
                self.set_case

            self.switch_player()
        
        self.winner.win()
        self.loser.lose()

    @property
    def winner(self) :
        if self.is_game_over :
            return self.player1 if self.score[self.player1.__str__()] > self.score[self.player2.__str__()] else self/self.player2
    
    @property
    def loser(self) :
        if self.is_game_over :
            return self.player1 if self.score[self.player1.__str__()] < self.score[self.player2.__str__()] else self/self.player2

    def get_model_data(self) :
        return {
            "grid_size" : self.grid_size ,
            "grid" : "" + self.grid ,
            "players" : self.score ,
            "player_coord" : [self.player1.coord, self.player2.coord] ,
            "player_color" : [self.player1.color, self.player1.color]
        }