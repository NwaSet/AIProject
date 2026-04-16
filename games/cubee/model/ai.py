import random
from .player import Player
from games.cubee.dao.dao import Dao


class Ia(Player):
    """
    AI player using Q-learning.

    Reward system:
    - self.penalty every move
    - +self.take_cell for each point gained
    - +self.win_reward on win
    - +self.lose_reward on lose
    """

    ACTION_TO_MOVE = {
        "up": (0, -1),
        "down": (0, 1),
        "left": (-1, 0),
        "right": (1, 0),
    }

    MOVE_TO_ACTION = {
        (0, -1): "up",
        (0, 1): "down",
        (-1, 0): "left",
        (1, 0): "right",
    }

    COMMIT_EVERY_GAMES = 5000

    def __init__(
        self,
        id: int,
        name: str,
        game: object = None,
        epsilon: float = 0.9,
        lr: float = 0.01,
        gamma: float = 0.7,
    ) -> None:
        """
        Initialize the AI player and its Q-learning settings.
        """
        super().__init__(id, name, game)

        self.color = "gray"

        self.win_reward = 5.0
        self.lose_reward = -5.0
        self.penalty = -0.5
        self.take_cell = 1.0

        self.epsilon = epsilon
        self.learning_rate = lr
        self.gamma = gamma

        self.legal_moves = []
        self.dao = Dao(f"lr{self.learning_rate}_g{self.gamma}")

        self.last_state = None
        self.last_action = None
        self.last_score = 0

        self.games_since_commit = 0

        self.q_cache = {}

    def move_to_string(self, move: tuple[int, int]) -> str:
        """
        Convert a move tuple into an action string.
        """
        return self.MOVE_TO_ACTION[move]

    def string_to_move(self, action: str) -> tuple[int, int]:
        """
        Convert an action string into a move tuple.
        """
        return self.ACTION_TO_MOVE[action]

    def state_key(self, state: dict) -> tuple:
        """
        Immutable key for state caching.
        """
        return (
            state["current_player"],
            state["player1_coord"],
            state["player2_coord"],
            state["grid"],
            state["grid_size"],
        )

    def get_current_score(self) -> int:
        """
        Return current score of this AI.
        """
        return self.game.score[str(self)]

    def set_legal_moves(self) -> list[str]:
        """
        Set legal moves from the real current game state.
        """
        self.legal_moves = [
            self.move_to_string(move)
            for move in self.game.legal_move()
        ]
        return self.legal_moves

    def legal_actions_from_state(self, state: dict) -> list[str]:
        """
        Compute legal actions only from a DTO state.
        """
        grid_size = state["grid_size"]
        current_player = state["current_player"]

        if current_player == self.game.player1.id:
            pos_index = state["player1_coord"]
        else:
            pos_index = state["player2_coord"]

        y, x = divmod(pos_index, grid_size)
        grid = state["grid"]

        legal_actions = []

        for action, (dx, dy) in self.ACTION_TO_MOVE.items():
            nx = x + dx
            ny = y + dy

            if 0 <= nx < grid_size and 0 <= ny < grid_size:
                idx = ny * grid_size + nx
                cell = int(grid[idx])

                if cell == 0 or cell == current_player:
                    legal_actions.append(action)

        return legal_actions

    def build_default_q_values(self, legal_actions: list[str]) -> dict:
        """
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

    def ensure_state_cached(self, state: dict) -> dict:
        """
        Return Q-values from cache, DB, or create default values.
        """
        key = self.state_key(state)

        if key in self.q_cache:
            return self.q_cache[key]

        q_values = self.dao.select_row_by_dto(state)
        if q_values is not None:
            self.q_cache[key] = q_values
            return q_values

        legal_actions = self.legal_actions_from_state(state)
        default_q_values = self.build_default_q_values(legal_actions)

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

        self.dao.stage_insert_if_missing(row_data)
        self.q_cache[key] = default_q_values.copy()
        return self.q_cache[key]

    def explore(self) -> str:
        """
        Choose a random legal action.
        """
        return random.choice(self.legal_moves)

    def exploit(self, q_values: dict) -> str:
        """
        Choose the best legal action according to Q-values.
        """
        best_actions = []
        max_value = float("-inf")

        for action in self.legal_moves:
            value = q_values[action]

            if value > max_value:
                max_value = value
                best_actions = [action]
            elif value == max_value:
                best_actions.append(action)

        if not best_actions:
            return random.choice(self.legal_moves)

        return random.choice(best_actions)

    def get_reward(self, last_score: int, new_score: int) -> float:
        """
        Reward the previous move.

        Base penalty every turn + reward for each point gained.
        """
        gained_points = new_score - last_score
        return self.penalty + (gained_points * self.take_cell)

    def learn(self, reward: float, next_state: dict | None = None) -> None:
        """
        Learn from the previous state/action.

        If next_state is None, this is a terminal update.
        """
        if self.last_state is None or self.last_action is None:
            return

        current_q_values = self.ensure_state_cached(self.last_state)
        old_value = current_q_values[self.last_action]

        if next_state is None:
            max_next = 0.0
        else:
            next_q_values = self.ensure_state_cached(next_state)
            legal_next_actions = self.legal_actions_from_state(next_state)
            max_next = max(
                (next_q_values[action] for action in legal_next_actions),
                default=0.0,
            )

        new_value = old_value + self.learning_rate * (
            reward + self.gamma * max_next - old_value
        )

        current_q_values[self.last_action] = new_value
        self.dao.stage_q_update(self.last_state, current_q_values)

    def play(self) -> tuple[int, int]:
        """
        Learn from the previous move using the current game state,
        then choose and return a move tuple.
        """
        state = self.game.get_state_dto()
        current_score = self.get_current_score()

        # on récompense le move précédent avec le nouvel état observé
        if self.last_state is not None and self.last_action is not None:
            reward = self.get_reward(self.last_score, current_score)
            self.learn(reward, state)

        self.set_legal_moves()
        current_q_values = self.ensure_state_cached(state)

        if random.random() < self.epsilon:
            action = self.explore()
        else:
            action = self.exploit(current_q_values)

        self.last_state = state
        self.last_action = action
        self.last_score = current_score

        return self.string_to_move(action)

    def end_episode(self) -> None:
        """
        Reset episode memory and flush every X games.
        """
        self.last_state = None
        self.last_action = None
        self.last_score = 0

        self.games_since_commit += 1
        if self.games_since_commit >= self.COMMIT_EVERY_GAMES:
            self.dao.flush()
            self.games_since_commit = 0

    def win(self) -> None:
        """
        Final terminal learn on win, then increment stats.
        """
        self.learn(self.win_reward, None)
        super().win()
        self.end_episode()

    def lose(self) -> None:
        """
        Final terminal learn on lose, then increment stats.
        """
        self.learn(self.lose_reward, None)
        super().lose()
        self.end_episode()

    def tie(self) -> None:
        """
        End of episode on tie.
        Neutral terminal reward.
        """
        self.learn(0.0, None)
        super().tie()
        self.end_episode()

    def force_commit(self) -> None:
        """
        Force write pending data to DB.
        Call this at the end of training.
        """
        self.dao.flush()
        self.games_since_commit = 0

    def next_epsilon(self, coefficient: float = 0.95, minimum: float = 0.05) -> float:
        """
        Decrease epsilon while keeping it above a minimum.
        """
        self.epsilon = max(minimum, self.epsilon * coefficient)
        return self.epsilon
