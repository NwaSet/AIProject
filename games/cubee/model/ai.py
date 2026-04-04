import random
from collections import deque
from .player import Player
from games.cubee.dao.dao import Dao


class Ia(Player):
    """
    AI player using Q-learning.

    Reward system:
    - always -0.5
    - +1 if the AI takes an empty cell
    - +5 if the AI wins
    """

    def __init__(
        self,
        id: int,
        name: str,
        game: object = None,
        epsilon: float = 0.9,
        lr: float = 0.01,
        gamma: float = 0.7,
    ) -> None:
        super().__init__(id, name, game)
        self.color = "gray"

        self.win_reward = 5
        self.penalty = -0.5
        self.take_cell = 1
        self.game = None
        self.epsilon = epsilon
        self.learning_rate = lr
        self.gamma = gamma

        self.dao = Dao(f"lr{self.learning_rate}_g{self.gamma}")

        self.last_state = None
        self.last_action = None
        self.next_state = None

    def move_to_string(self, move: tuple[int, int]) -> str:
        """
        Convert a move tuple into a string.
        """
        return {
            (0, -1): "up",
            (0, 1): "down",
            (-1, 0): "left",
            (1, 0): "right",
        }[move]

    def string_to_move(self, action: str) -> tuple[int, int]:
        """
        Convert an action string into a move tuple.
        """
        return {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }[action]

    def rebuild_grid(self, state: dict) -> list[list[int]]:
        """
        Rebuild the 2D grid from the DTO.
        """
        grid_size = state["grid_size"]
        flat_grid = [int(cell) for cell in state["grid"]]

        return [
            flat_grid[i : i + grid_size] for i in range(0, len(flat_grid), grid_size)
        ]

    def index_to_coord(self, index: int, grid_size: int) -> tuple[int, int]:
        """
        Convert flattened index into (x, y).
        """
        y, x = divmod(index, grid_size)
        return x, y

    def coord_to_index(self, x: int, y: int, grid_size: int) -> int:
        """
        Convert (x, y) into flattened index.
        """
        return y * grid_size + x

    def update_enclosure(self, grid: list[list[int]]) -> None:
        """
        Apply the same enclosure capture rules as GameModel on a simulated grid.
        """

        grid_size = len(grid)
        visited = [[False for _ in range(grid_size)] for _ in range(grid_size)]

        player1_id = 1
        player2_id = 2

        if self.game is not None:
            player1_id = self.game.player1.id
            player2_id = self.game.player2.id

        directions = ((0, -1), (0, 1), (-1, 0), (1, 0))

        for row in range(grid_size):
            for col in range(grid_size):
                if grid[row][col] != 0 or visited[row][col]:
                    continue

                zone = []
                queue = deque([(col, row)])
                touches_p1 = False
                touches_p2 = False

                while queue:
                    c, r = queue.popleft()

                    if visited[r][c]:
                        continue

                    visited[r][c] = True
                    zone.append((c, r))

                    for dcol, drow in directions:
                        nc, nr = c + dcol, r + drow

                        if 0 <= nc < grid_size and 0 <= nr < grid_size:
                            if grid[nr][nc] == 0:
                                queue.append((nc, nr))
                            elif grid[nr][nc] == player1_id:
                                touches_p1 = True
                            elif grid[nr][nc] == player2_id:
                                touches_p2 = True

                if touches_p1 and not touches_p2:
                    owner = player1_id
                elif touches_p2 and not touches_p1:
                    owner = player2_id
                else:
                    continue

                for c, r in zone:
                    grid[r][c] = owner

    def legal_actions(self) -> list[str]:
        """
        Return legal actions from the real current game state.
        """
        return [self.move_to_string(move) for move in self.game.legal_move()]

    def legal_actions_from_state(self, state: dict) -> list[str]:
        """
        Return legal actions for a simulated state, without using the real model.
        A move is legal if it stays inside the grid and lands on:
        - an empty cell (0)
        - or a cell already owned by the current player
        """

        grid_size = state["grid_size"]
        grid = self.rebuild_grid(state)

        if state["current_player"] == 1:
            px, py = self.index_to_coord(state["player1_coord"], grid_size)
        else:
            px, py = self.index_to_coord(state["player2_coord"], grid_size)

        legal_actions = []

        for action, (dx, dy) in {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }.items():
            nx, ny = px + dx, py + dy

            if 0 <= nx < grid_size and 0 <= ny < grid_size:
                if grid[ny][nx] in (0, state["current_player"]):
                    legal_actions.append(action)

        return legal_actions

    def build_default_q_values(self, legal_actions: list[str]) -> dict:
        """
        Build default Q-values.

        Legal actions start at 0.0.
        Illegal actions start at penalty.
        """

        q_values = {
            "up": self.penalty,
            "down": self.penalty,
            "left": self.penalty,
            "right": self.penalty,
        }

        for action in legal_actions:
            q_values[action] = 0.0

        return q_values

    def ensure_current_state(self, state: dict) -> dict:
        """
        Ensure current state exists in DB.
        If missing, insert it with default values.
        """

        q_values = self.dao.select_row_by_dto(state)
        if q_values is not None:
            return q_values

        default_q_values = self.build_default_q_values(self.legal_actions())

        row_data = {
            "current_player": state["current_player"],
            "player1_coord": state["player1_coord"],
            "player2_coord": state["player2_coord"],
            "grid": state["grid"],
            "grid_size": state["grid_size"],
            "up": default_q_values["up"],
            "down": default_q_values["down"],
            "left": default_q_values["left"],
            "right": default_q_values["right"],
        }

        self.dao.add_row(row_data)
        return default_q_values.copy()

    def get_next_q_values(self, next_state: dict) -> dict:
        """
        Get next state Q-values.

        Important:
        - if next_state exists in DB, use it
        - otherwise, do NOT insert it
        - return default values computed from the simulated state
        """

        q_values = self.dao.select_row_by_dto(next_state)
        if q_values is not None:
            return q_values

        return self.build_default_q_values(self.legal_actions_from_state(next_state))

    def explore(self) -> str:
        """
        Choose a random legal action.
        """
        return random.choice(self.legal_actions())

    def exploit(self, q_values: dict) -> str:
        """
        Choose the best legal action according to Q-values.
        """

        legal_actions = self.legal_actions()
        best_actions = []
        max_value = float("-inf")

        for action in legal_actions:
            value = q_values[action]

            if value > max_value:
                max_value = value
                best_actions = [action]
            elif value == max_value:
                best_actions.append(action)
        
        if not best_actions :
            return random.choice(legal_actions)

        return random.choice(best_actions)

    def compute_reward(self, took_case: bool, win: bool) -> float:
        """
        Compute reward for the simulated move.
        """
        reward = self.penalty

        if took_case:
            reward += self.take_cell

        if win:
            reward += self.win_reward

        return reward

    def q_function(
        self,
        state: dict,
        current_q_values: dict,
        action: str,
        reward: float,
        next_state: dict,
    ) -> None:
        """
        Apply Q-learning update.

        Important:
        - update only current_state
        - do not create next_state here
        """

        next_q_values = self.get_next_q_values(next_state)

        old_value = current_q_values[action]
        legal_next_actions = self.legal_actions_from_state(next_state)
        max_next = max((next_q_values[a] for a in legal_next_actions), default=0.0)

        new_value = old_value + self.learning_rate * (
            reward + self.gamma * max_next - old_value
        )

        current_q_values[action] = new_value
        self.dao.update_row(state, current_q_values)

    def set_next_state(self, current_q_values: dict) -> None:
        """
        Simulate the chosen move, compute reward, and update the current state.

        Important:
        - only current_state is inserted/updated
        - next_state is only simulated
        """

        if self.last_state is None or self.last_action is None:
            return

        state = self.last_state
        grid_size = state["grid_size"]
        current_player = state["current_player"]

        grid = self.rebuild_grid(state)

        p1_x, p1_y = self.index_to_coord(state["player1_coord"], grid_size)
        p2_x, p2_y = self.index_to_coord(state["player2_coord"], grid_size)

        if current_player == 1:
            px, py = p1_x, p1_y
        else:
            px, py = p2_x, p2_y

        dx, dy = self.string_to_move(self.last_action)
        nx, ny = px + dx, py + dy

        took_case = grid[ny][nx] == 0
        grid[ny][nx] = current_player
        self.update_enclosure(grid)

        new_p1_coord = state["player1_coord"]
        new_p2_coord = state["player2_coord"]

        if current_player == 1:
            new_p1_coord = self.coord_to_index(nx, ny, grid_size)
        else:
            new_p2_coord = self.coord_to_index(nx, ny, grid_size)

        next_player = 2 if current_player == 1 else 1
        new_grid = "".join(str(cell) for row in grid for cell in row)

        self.next_state = {
            "current_player": next_player,
            "player1_coord": new_p1_coord,
            "player2_coord": new_p2_coord,
            "grid": new_grid,
            "grid_size": grid_size,
        }

        win = False
        if "0" not in new_grid:
            p1_score = new_grid.count("1")
            p2_score = new_grid.count("2")

            if self.id == 1:
                win = p1_score > p2_score
            else:
                win = p2_score > p1_score

        reward = self.compute_reward(took_case, win)
        self.q_function(
            state, current_q_values, self.last_action, reward, self.next_state
        )

    def play(self) -> tuple[int, int]:
        """
        Choose a move, simulate it, update current_state, then return the move.
        """

        self.last_state = self.game.get_state_dto()
        current_q_values = self.ensure_current_state(self.last_state)

        if random.random() < self.epsilon:
            self.last_action = self.explore()
        else:
            self.last_action = self.exploit(current_q_values)

        chosen_action = self.last_action
        self.set_next_state(current_q_values)
        move = self.string_to_move(chosen_action)

        self.last_state = None
        self.last_action = None
        self.next_state = None

        return move

    def next_epsilon(self, coefficient: float = 0.95, minimum: float = 0.05) -> float:
        """
        Decrease epsilon while keeping it above a minimum value.
        """
        self.epsilon = max(minimum, self.epsilon * coefficient)
        return self.epsilon
