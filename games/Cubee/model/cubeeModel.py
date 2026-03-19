import random
from games.Cubee.Player.Human import Human
from collections import deque


class GameModel:
    possible_direction = [
        (0, -1),  # up
        (0, 1),  # down
        (-1, 0),  # left
        (1, 0),  # right
    ]

    def __init__(
        self, grid_size, display=True, Player1=None, Player2=None, controler=None
    ):

        self.player1 = Player1
        self.player2 = Player2

        self.controler = controler
        self.controler.game = self

        self.grid_size = grid_size
        self.grid = []
        self.init_grid()

        self.display = display

        self.player1.coord = (self.grid_size - 1, self.grid_size - 1)
        self.player2.coord = (0, 0)

        self.score = {self.player1.__str__(): 1, self.player2.__str__(): 1}

        self.current_player = self.shuffle()

    def init_grid(self):
        for _ in range(self.grid_size):
            row = []
            for _ in range(self.grid_size):
                row.append(0)
            self.grid.append(row)
        self.grid[0][0] = self.player2.id
        self.grid[self.grid_size - 1][self.grid_size - 1] = self.player1.id

    def shuffle(self):
        return random.choice([self.player1, self.player2])

    def switch_player(self):
        self.current_player = (
            self.player1 if self.current_player == self.player2 else self.player2
        )

    def reset(self):

        self.grid = []
        self.init_grid()

        self.player1.coord = (self.grid_size - 1, self.grid_size - 1)
        self.player2.coord = (0, 0)

        self.current_player = self.shuffle()

        self.score = {self.player1.__str__(): 1, self.player2.__str__(): 1}

    def is_game_over(self):
        """
        check if the all grid is complet
        return true if the all grid is used else false
        """
        return all(0 not in row for row in self.grid)

    def legal_move(self):
        """
        verify all possible move for the player,
        return a list of tuple for all possible action == (x, y) .
        """
        player_coord_x, player_coord_y = self.current_player.coord

        legal_action = []

        for direction_x, direction_y in GameModel.possible_direction:
            new_x = player_coord_x + direction_x
            new_y = player_coord_y + direction_y

            if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
                if self.grid[new_y][new_x] in (0, self.current_player.id):
                    legal_action.append((direction_x, direction_y))

        return legal_action

    def set_case(self):
        p_x, p_y = self.current_player.coord
        if self.grid[p_y][p_x] == 0:
            self.grid[p_y][p_x] = self.current_player.id
            self.score[self.current_player.__str__()] += 1
        else:
            pass

    def set_player_coord(self, move):
        if not self.is_game_over():
            p_x, p_y = self.current_player.coord
            d_x, d_y = move
            self.current_player.coord = (p_x + d_x, p_y + d_y)

    def step(self, move):

        if move in self.legal_move():
            self.set_player_coord(move)
            self.set_case()
            self.update_enclos()
        if self.is_game_over():
            self.winner.win()
            self.loser.lose()
        else:
            self.switch_player()
            if not isinstance(self.current_player, Human):
                self.step(self.current_player.play())

    def bfs(self):
        visited = [
            [False for _ in range(self.grid_size)] for _ in range(self.grid_size)
        ]
        queue = deque()

        for i in range(self.grid_size):
            if self.grid[i][0] == 0:
                queue.append((0, i))
            if self.grid[i][self.grid_size - 1] == 0:
                queue.append((self.grid_size - 1, i))
            if self.grid[0][i] == 0:
                queue.append((i, 0))
            if self.grid[self.grid_size - 1][i] == 0:
                queue.append((i, self.grid_size - 1))

        while queue:
            col, row = queue.popleft()

            if visited[row][col]:
                continue

            visited[row][col] = True

            for dcol, drow in GameModel.possible_direction:
                ncol, nrow = col + dcol, row + drow

                if 0 <= ncol < self.grid_size and 0 <= nrow < self.grid_size:
                    if self.grid[nrow][ncol] == 0:
                        queue.append((ncol, nrow))

        return visited

    def update_enclos(self):
        visited = [
            [False for _ in range(self.grid_size)] for _ in range(self.grid_size)
        ]

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.grid[row][col] == 0 and not visited[row][col]:
                    zone = []
                    queue = deque()
                    queue.append((col, row))

                    touches_p1 = False
                    touches_p2 = False

                    while queue:
                        c, r = queue.popleft()

                        if visited[r][c]:
                            continue

                        visited[r][c] = True
                        zone.append((c, r))

                        for dcol, drow in GameModel.possible_direction:
                            nc, nr = c + dcol, r + drow

                            if 0 <= nc < self.grid_size and 0 <= nr < self.grid_size:
                                if self.grid[nr][nc] == 0:
                                    queue.append((nc, nr))

                                elif self.grid[nr][nc] == self.player1.id:
                                    touches_p1 = True

                                elif self.grid[nr][nc] == self.player2.id:
                                    touches_p2 = True

                    if touches_p1 and not touches_p2:
                        owner = self.player1.id
                    elif touches_p2 and not touches_p1:
                        owner = self.player2.id
                    else:
                        continue

                    for c, r in zone:
                        self.grid[r][c] = owner
                        if owner == self.player1.id:
                            self.score[self.player1.__str__()] += 1
                        else:
                            self.score[self.player2.__str__()] += 1

    def play(self):

        while not self.is_game_over():
            move = self.current_player.play()
            if move in self.legal_move():
                self.set_player_coord(move)
                self.set_case()
                self.update_enclos()
            self.switch_player()

        self.winner.win()
        self.loser.lose()

    @property
    def winner(self):
        if self.is_game_over:
            return (
                self.player1
                if self.score[self.player1.__str__()]
                > self.score[self.player2.__str__()]
                else self.player2
            )

    @property
    def loser(self):
        if self.is_game_over:
            return (
                self.player1
                if self.score[self.player1.__str__()]
                < self.score[self.player2.__str__()]
                else self.player2
            )

    def get_model_data(self):
        return {
            "grid_size": self.grid_size,
            "grid": self.grid,
            "players": self.score,
            "current_player": self.current_player,
            "player_coord": [self.player1.coord, self.player2.coord],
            "player_color": [self.player1.color, self.player2.color],
            "player_id": [self.player1.id, self.player2.id],
        }

