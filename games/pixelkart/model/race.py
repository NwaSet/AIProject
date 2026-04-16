from games.pixelkart.const import *
from games.pixelkart.model.circuit import *
from games.pixelkart.model.human import Human
import random

class Race:
   
    def __init__(
        self,
        circuit: object,
        nb_max_lap: int,
        display: bool = True,
        Player1: object = None,
        Player2: object = None
    ):   
        self.display = display

        self.circuit = circuit  

        self.player1 = Player1
        self.player2 = Player2

        self.player1.game = self
        self.player2.game = self

        self.current_player = self.shuffle()

        self.nb_round = 0

        self.nb_max_lap = nb_max_lap

        self.coord_starter = self.search_starter()
        self.init_pos()

        if self.display and not isinstance(self.current_player, Human) :
            self.step(self.current_player.play())
    

    def is_legal_move(self,current_action, next_action):
    
        current_vec = ACTION_TO_MOVE[current_action]
        next_vec = ACTION_TO_MOVE[next_action]

        dot = current_vec[0]*next_vec[0] + current_vec[1]*next_vec[1]

        return dot != -1
    
    def change_direction(self, direction):
        if self.is_legal_move(self.current_player.direction,direction):
            self.current_player.direction = direction

    def change_speed(self,speed):
        player = self.current_player
        if player.speed + speed > 2:
            player.speed = 2
        elif player.speed + speed < -1:
            player.speed = -1
        else:
            player.speed += speed

    def update_lap(self, player):
        if player.direction == "East":    
            row, col = player.coord
            current_cell = self.circuit.grid[row][col]

            if player.last_cell is None:
                player.last_cell = current_cell
                return

            if player.last_cell != "F" and current_cell == "F":
                player.lap += 1

            player.last_cell = current_cell
            
    def change_pos(self, player):
        d_row, d_col = ACTION_TO_MOVE[player.direction]
        row, col = player.coord

        speed = player.speed
        speed_factor = speed if self.circuit.grid[row][col] != "G" else speed / 2

        new_row = int(row + d_row * speed_factor)
        new_col = int(col + d_col * speed_factor)

        if not (0 <= new_row < len(self.circuit.grid) and 0 <= new_col < len(self.circuit.grid[0])):
            return

        if self.circuit.grid[new_row][new_col] == "W":
            return

        player.coord = (new_row, new_col)


    
    def shuffle(self) -> object:
        """
        return a random player to be the current player
        """

        return random.choice([self.player1, self.player2])
    
    def switch_player(self) -> None:
        """
        switch the current player between the 2 players
        """

        self.current_player = (
            self.player1 if self.current_player == self.player2 else self.player2
        )

    def search_starter(self):
        starters = []
        for row in range(len(self.circuit.grid)):
            for col in range(len(self.circuit.grid[row])):
                if self.circuit.grid[row][col] == "F":
                    starters.append((row, col))
        return starters


    def init_pos(self):
        if len(self.coord_starter) < 2:
            raise ValueError("A circuit needs at least two finish cells to place the players.")

        starter = self.coord_starter.copy()
        
        self.player1.coord = random.choice(starter)
        starter.remove(self.player1.coord)
        self.player2.coord = random.choice(starter)

        self.player1.direction = "East"
        self.player2.direction = "East"

        self.player1.lap = 0
        self.player2.lap = 0

        self.player1.last_cell = None
        self.player2.last_cell = None


    def is_game_over(self):
        return (
            self.player1.lap >= self.nb_max_lap or
            self.player2.lap >= self.nb_max_lap
        )
    
    def step(self, move) :
        if self.is_game_over():
            return

        player = self.current_player

        if move == "pass_turn":
            pass
        elif move == "accelerate":
            self.change_speed(1)
        elif move == "decelerate":
            self.change_speed(-1)
        elif move in {"turn_left", "turn_right"}:
            match self.current_player.direction:
                case "North":
                    move_action = NORTH_TO_MOVE[move]
                case "South":
                    move_action = SOUTH_TO_MOVE[move]
                case "East":
                    move_action = EAST_TO_MOVE[move]
                case "West":
                    move_action = WEST_TO_MOVE[move]
            self.change_direction(move_action)
        elif move in ACTION_TO_MOVE:
            self.change_direction(move)
        elif isinstance(move, int):
            self.change_speed(move)
        else:
            raise ValueError(f"Unknown move: {move}")

        self.change_pos(player)
        self.nb_round += 1
        self.update_lap(player)
        
        if self.is_game_over():
            if self.winner is None:
                self.player1.tie()
                self.player2.tie()
            else:
                self.winner.win()
                self.loser.lose()
        else:
            self.switch_player()

            if self.display and not isinstance(self.current_player, Human) :
                self.step(self.current_player.play())

    def play(self):
        while not self.is_game_over():
            self.step(self.current_player.play())

    @property
    def winner(self):
        if self.player1.lap > self.player2.lap:
            return self.player1
        elif self.player2.lap > self.player1.lap:
            return self.player2
        return None
    
    @property
    def loser(self):
        if self.player1.lap < self.player2.lap:
            return self.player1
        elif self.player2.lap < self.player1.lap:
            return self.player2
        return None
            
    def race_dto(self):
        return {
            "player_coord":[self.player1.coord, self.player2.coord],
            "nb_lap": self.nb_max_lap
        }
    
    def to_dto(self) :
        """
        return the dto of the game

        {
            "grid": "GGGG,GRRG,GGGG",
            "player1_pos": (row, col),
            "player2_pos": (row, col),
            "player1_name": "...",
            "player2_name": "...",
            "player1_speed": 0,
            "player2_speed": 0,
            "player1_laps": 0,
            "player2_laps": 0,
            "current_player": 1
        }
        """
        return {
            "grid": self.circuit.grid_str,
            "player1_pos": self.player1.coord,
            "player2_pos": self.player2.coord,
            "player1_name": self.player1.name,
            "player2_name": self.player2.name,
            "player1_color": self.player1.color,
            "player2_color": self.player2.color,
            "player1_speed": self.player1.speed,
            "player2_speed": self.player2.speed,
            "player1_laps": self.player1.lap,
            "player2_laps": self.player2.lap,
            "current_player": self.current_player.id
        }
