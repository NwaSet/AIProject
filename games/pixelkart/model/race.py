from games.pixelkart.const import *
from games.pixelkart.model.circuit import *
import random

class Race:
   
    def __init__(
        self,
        circuit: object,
        nb_max_lap: int,
        display: bool = True,
        controler: object = None,
        Player1: object = None,
        Player2: object = None
    ):   
        self.circuit = circuit  
        self.controler = controler

        self.player1 = Player1
        self.player2 = Player2

        self.player1.game = self
        self.player2.game = self

        self.current_player = self.shuffle()

        self.nb_round = 0

        self.nb_max_lap = nb_max_lap

        self.coord_starter = self.search_starter()
    

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
            x, y = player.coord
            current_cell = self.circuit.grid[y][x]

            if player.last_cell is None:
                player.last_cell = current_cell
                return

            if player.last_cell != "F" and current_cell == "F":
                player.lap += 1

            player.last_cell = current_cell
            
    def change_pos(self, player):
        dx, dy = ACTION_TO_MOVE[player.direction]
        x, y = player.coord

        speed = player.speed
        speed_factor = speed if self.circuit.grid[y][x] != "G" else speed / 2

        new_x = int(x + dx * speed_factor)
        new_y = int(y + dy * speed_factor)

        if not (0 <= new_y < len(self.circuit.grid) and 0 <= new_x < len(self.circuit.grid[0])):
            return

        if self.circuit.grid[new_y][new_x] == "W":
            return

        player.coord = (new_x, new_y)


    
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
        for y in range(len(self.circuit.grid)):
            for x in range(len(self.circuit.grid[y])):
                if self.circuit.grid[y][x] == "W":
                    starters.append((x, y))
        return starters


    def init_pos(self):
        starter = self.coord_starter
        
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
        action = SETTINGS_TO_ACTION[move]

        # if we pass
        if action == "pass_turn" :
            pass
        
        # if we change speed :
        elif type(action) == int:
                self.change_speed(action)
        
        # if we change direction 
        elif type(action) == str:
                    match self.current_player.direction :
                        case "North" :
                            move_action = NORTH_TO_MOVE[action]
                        case "South" :
                            move_action = SOUTH_TO_MOVE[action]
                        case "East" :
                            move_action = EAST_TO_MOVE[action]
                        case "West" :
                            move_action = WEST_TO_MOVE[action]
                    self.change_direction(move_action)
        
        self.change_pos(self.current_player)
        self.switch_player()
        self.nb_round += 1
        self.update_lap(self.current_player)
        
        if self.is_game_over() :
            if self.winner is None:
                self.player1.tie()
                self.player2.tie()
            else:
                self.winner.win()
                self.loser.lose()
        else :
            self.switch_player()

    def play(self):
        while not self.is_game_over():
            player = self.current_player
            move = player.play()
            
            if type(move) == str:
                    self.change_direction(move)
            elif type(move) == int:
                self.change_speed(move)
            
            self.change_pos(player)
            self.switch_player()
            self.nb_round += 1
            self.update_lap(player)

        if self.winner is None:
            self.player1.tie()
            self.player2.tie()
        else:
            self.winner.win()
            self.loser.lose()

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
            "nb_lap": self.nb_lap_game
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
            "player1_speed": self.player1.speed,
            "player2_speed": self.player2.speed,
            "player1_laps": self.player1.lap,
            "player2_laps": self.player2.lap,
            "current_player": self.current_player.id
        }