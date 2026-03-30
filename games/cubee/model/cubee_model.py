import random
from games.cubee.player.human import Human
from games.cubee.player.ai import Ia

from collections import deque


class GameModel :

    """
    Represent the main model of the Cubee game.

    This class manages:
    - the game grid
    - the two players
    - player positions
    - scores
    - turn management
    - move validation
    - territory capture logic
    - end-game detection

    Attributes:
        possible_direction (list[tuple[int, int]]): List of all possible movement
            directions: up, down, left, and right.
        player1 (Player): First player of the game.
        player2 (Player): Second player of the game.
        controler (gameControler): Controller associated with the model.
        grid_size (int): Size of the square grid.
        grid (list[list[int]]): 2D grid representing the board.
        display (bool): Indicates whether the game should be displayed.
        score (dict): Dictionary containing each player's score.
        current_player (Player): Player whose turn it is.
    """

    possible_direction = [
        (0, -1),  # up
        (0, 1),  # down
        (-1, 0),  # left
        (1, 0),  # right
    ]

    def __init__(
            self,
            grid_size: int,
            display: bool = True,
            Player1: object = None,
            Player2: object = None,
            controler: object = None,
            ) -> None :
        """
        Initialize the game model.

        Args:
            grid_size (int): Size of the square grid.
            display (bool, optional): Whether the game is displayed. Defaults to True.
            Player1 (Player, optional): First player. Defaults to None.
            Player2 (Player, optional): Second player. Defaults to None.
            controler (gameControler, optional): Controller associated with the model.
                Defaults to None.
        """

        self.player1 = Player1
        self.player2 = Player2

        self.player1.game = self
        self.player2.game = self

        self.controler = controler
        if self.controler != None :
            self.controler.game = self

        self.grid_size = grid_size
        self.grid = []
        self.init_grid()

        self.display = display

        self.player1.coord = (self.grid_size - 1, self.grid_size - 1)
        self.player2.coord = (0, 0)

        self.score = {self.player1.__str__(): 1, self.player2.__str__(): 1}

        self.current_player = self.shuffle()


    def init_grid(self) -> None :
        """
        Initialize the game grid.

        Creates an empty square grid filled with 0, then places:
        - player 2 in the top-left corner
        - player 1 in the bottom-right corner
        """

        for _ in range(self.grid_size) :
            row = []
            for _ in range(self.grid_size) :
                row.append(0)
            self.grid.append(row)
        self.grid[0][0] = self.player2.id
        self.grid[self.grid_size - 1][self.grid_size - 1] = self.player1.id


    def shuffle(self) -> object :
        """
        return a random player to be the current player
        """

        return random.choice([self.player1, self.player2])

    def switch_player(self) -> None :
        """
        switch the current player between the 2 players
        """

        self.current_player = (
            self.player1 if self.current_player == self.player2 else self.player2
        )


    def reset(self) -> None :
        """
        reset the grid
        replace both players
        put their score at 1
        """

        self.grid = []
        self.init_grid()

        self.player1.coord = (self.grid_size - 1, self.grid_size - 1)
        self.player2.coord = (0, 0)

        self.current_player = self.shuffle()

        self.score = {self.player1.__str__(): 1, self.player2.__str__(): 1}


    def is_game_over(self) -> bool :
        """
        check if the all grid is complet
        return true if the all grid is used else false
        """

        return all(0 not in row for row in self.grid)

    def legal_move(self) -> list[tuple] :
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
                if self.grid[new_y][new_x] in (0, self.current_player.id) :
                    legal_action.append((direction_x, direction_y))

        return legal_action


    def set_cell(self) -> None :
        """
        set the cell where the current player is with his id
        """

        p_x, p_y = self.current_player.coord
        if self.grid[p_y][p_x] == 0 :
            self.grid[p_y][p_x] = self.current_player.id
            self.score[self.current_player.__str__()] += 1
        else :
            pass


    def set_player_coord(
            self,
            move: tuple
            ) -> None :
        """
        set the current player with the new coord
        """

        if not self.is_game_over() :
            p_x, p_y = self.current_player.coord
            d_x, d_y = move
            self.current_player.coord = (p_x + d_x, p_y + d_y)


    def step(
            self,
            move: tuple
            ) -> None :
        """
        Execute one turn of the game.

        If the move is legal:
        - update the player's coordinates
        - mark the new cell
        - update enclosed areas

        Then:
        - if the game is over, update winner and loser statistics
        - otherwise switch to the next player
        - if the next player is an AI, automatically play its turn

        Args:
            move (tuple[int, int]): Move chosen by the current player.
        """

        if move in self.legal_move() :
            self.set_player_coord(move)
            self.set_cell()
            self.update_enclosure()
        if self.is_game_over() :
            self.winner.win()
            self.loser.lose()
        else :
            self.switch_player()
            if not isinstance(self.current_player, Human) :
                self.step(self.current_player.play())


    def update_enclosure(self) -> None :
        """
        Detect and fill enclosed empty zones.

        This method uses a breadth-first search (BFS) to explore each empty zone.
        An empty zone is assigned to a player if it touches only that player's
        cells and not the opponent's cells.

        When a zone is captured:
        - the cells are filled with the owner's id
        - the owner's score is increased accordingly
        """

        visited = [
            [False for _ in range(self.grid_size)] for _ in range(self.grid_size)
        ]

        for row in range(self.grid_size) :
            for col in range(self.grid_size) :
                if self.grid[row][col] == 0 and not visited[row][col] :
                    zone = []
                    queue = deque()
                    queue.append((col, row))

                    touches_p1 = False
                    touches_p2 = False

                    while queue :
                        c, r = queue.popleft()

                        if visited[r][c] :
                            continue

                        visited[r][c] = True
                        zone.append((c, r))

                        for dcol, drow in GameModel.possible_direction:
                            nc, nr = c + dcol, r + drow

                            if 0 <= nc < self.grid_size and 0 <= nr < self.grid_size :
                                if self.grid[nr][nc] == 0 :
                                    queue.append((nc, nr))

                                elif self.grid[nr][nc] == self.player1.id :
                                    touches_p1 = True

                                elif self.grid[nr][nc] == self.player2.id :
                                    touches_p2 = True

                    if touches_p1 and not touches_p2 :
                        owner = self.player1.id
                    elif touches_p2 and not touches_p1 :
                        owner = self.player2.id
                    else :
                        continue

                    for c, r in zone :
                        self.grid[r][c] = owner
                        if owner == self.player1.id :
                            self.score[self.player1.__str__()] += 1
                        else :
                            self.score[self.player2.__str__()] += 1


    def play(self) -> None :
        """
        Run a full automatic game until completion.

        At each turn:
        - the current player chooses a move
        - the move is applied if legal
        - the board and enclosed areas are updated
        - the turn is passed to the next player

        Once the game ends:
        - the winner's statistics are updated
        - the loser's statistics are updated
        """

        while not self.is_game_over() :
            player = self.current_player
            move = player.play()

            info = self.play_ai_step(move)

            if isinstance(player, Ia) :
                player.update_after_move(info)

        self.winner.win()
        self.loser.lose()


    @property
    def winner(self) -> object :
        """
        return the winner of the game
        if game is over
        """

        if self.is_game_over() :
            return (
                self.player1
                if self.score[self.player1.__str__()] > self.score[self.player2.__str__()]
                else self.player2
            )


    @property
    def loser(self) -> object :
        """
        return the loser of the game
        if game is over
        """

        if self.is_game_over() :
            return (
                self.player1
                if self.score[self.player1.__str__()] < self.score[self.player2.__str__()]
                else self.player2
            )


    def play_ai_step(
            self,
            move : tuple[int,int]
            ) -> None :
        """
        step ai version,
        return info after the move to update the q-table.
        """

        info = {"took_case": False, "win": False, "lose": False}

        old_score = self.score[self.current_player.__str__()]

        if move in self.legal_move() :
            self.set_player_coord(move)
            self.set_cell()
            self.update_enclosure()

            new_score = self.score[self.current_player.__str__()]
            if new_score > old_score :
                info["took_case"] = True

        if self.is_game_over() :
            if self.winner == self.current_player :
                info["win"] = True
            else :
                info["lose"] = True

        else :
            self.switch_player()

        return info


    def get_state_dto(self) -> dict :
        """
        return state of the game that the ai and the dao will need
        """

        return {
            "current_player": self.current_player.id,
            "player1_coord": self.player1.coord[0] * self.grid_size + self.player1.coord[1],
            "player2_coord": self.player2.coord[0] * self.grid_size + self.player2.coord[1],
            "grid": "".join(str(cell) for row in self.grid for cell in row),
            "grid_size": self.grid_size,
        }


    def get_model_data(self) -> dict :
        """
        send the model data needed by the view
        """
        
        return {
            "grid_size": self.grid_size,
            "grid": self.grid,
            "players": self.score,
            "current_player": self.current_player,
            "player_coord": [self.player1.coord, self.player2.coord],
            "player_color": [self.player1.color, self.player2.color],
            "player_id": [self.player1.id, self.player2.id],
        }
