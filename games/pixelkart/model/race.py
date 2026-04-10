from pixelkart.const import *

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
            current_cell = self.circuit[y][x]

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
        speed_factor = speed if self.circuit[y][x] != "G" else speed / 2

        new_x = int(x + dx * speed_factor)
        new_y = int(y + dy * speed_factor)

        if not (0 <= new_y < len(self.circuit) and 0 <= new_x < len(self.circuit[0])):
            return

        if self.circuit[new_y][new_x] == "W":
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
        for y in range(len(self.circuit)):
            for x in range(len(self.circuit[y])):
                if self.circuit[y][x] == "W":
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