import random

from games.pixelkart.const import ACTION_TO_MOVE
from games.pixelkart.dao.dao import Dao
from games.pixelkart.model.kart import Kart


class Ai(Kart):
    """
    PixelKart AI using Q-learning with a SQLite-backed Q-table.
    """

    COMMIT_EVERY_GAMES = 5000

    def __init__(
        self,
        id: int,
        name: str,
        game: object = None,
        epsilon: float = 0.9,
        lr: float = 0.01,
        gamma: float = 0.7,
        learning_enabled: bool = True,
        db_name: str | None = None,
    ) -> None:
        super().__init__(id, name, game)

        self.color = "Red"

        self.epsilon = epsilon
        self.learning_rate = lr
        self.gamma = gamma
        self.learning_enabled = learning_enabled

        self.turn_count = 0
        self.last_lap_turn = 0
        self.last_reward = 0.0

        self.step_penalty = -0.01
        self.backward_lap_penalty = -20.0
        self.win_reward = 50.0
        self.lose_reward = -50.0
        self.lap_reward_base = 100.0
        self.penalty = -10.0

        self.last_state = None
        self.last_action = None
        self.games_since_commit = 0

        self.dao = Dao(db_name or f"lr{self.learning_rate}_g{self.gamma}")
        self.q_cache = {}

    def get_reward(self) -> float:
        """
        Return the reward produced by the last action.
        """
        return self.last_reward

    def get_state(self) -> tuple:
        """
        Return the current state seen by the AI.
        """
        return (
            self.coord,
            self.direction,
            self.speed,
            *self.get_surrounding_cells(),
        )

    def get_cell_value(self, row: int, col: int) -> str:
        """
        Return the cell content or OUT if outside the grid.
        """
        grid = self.game.circuit.grid

        if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
            return grid[row][col]

        return "OUT"

    def get_surrounding_cells(self) -> tuple:
        """
        Return the cells around the kart relative to its direction.
        """
        row, col = self.coord
        dr, dc = ACTION_TO_MOVE[self.direction]

        left_r, left_c = -dc, dr
        right_r, right_c = dc, -dr
        back_r, back_c = -dr, -dc

        front_1 = self.get_cell_value(row + dr, col + dc)
        front_2 = self.get_cell_value(row + 2 * dr, col + 2 * dc)
        front_3 = self.get_cell_value(row + 3 * dr, col + 3 * dc)

        left_1 = self.get_cell_value(row + left_r, col + left_c)
        left_2 = self.get_cell_value(row + 2 * left_r, col + 2 * left_c)
        left_3 = self.get_cell_value(row + 3 * left_r, col + 3 * left_c)

        right_1 = self.get_cell_value(row + right_r, col + right_c)
        right_2 = self.get_cell_value(row + 2 * right_r, col + 2 * right_c)
        right_3 = self.get_cell_value(row + 3 * right_r, col + 3 * right_c)

        back_1 = self.get_cell_value(row + back_r, col + back_c)

        return (
            front_1,
            front_2,
            front_3,
            left_1,
            left_2,
            left_3,
            right_1,
            right_2,
            right_3,
            back_1,
        )

    def get_legal_actions(self) -> list[str]:
        """
        Return legal actions from the current state.
        """
        return self.get_legal_actions_from_state(self.get_state())

    def get_legal_actions_from_state(self, state: tuple) -> list[str]:
        """
        Return legal actions from a given state tuple.
        """
        speed = state[2]

        legal_actions = ["pass_turn", "turn_left", "turn_right"]

        if speed < 2:
            legal_actions.append("accelerate")

        if speed > -1:
            legal_actions.append("decelerate")

        return legal_actions

    def build_default_q_values(self, legal_actions: list[str]) -> dict:
        """
        Build default Q-values for one state.
        """
        q_values = {
            "pass_turn": self.penalty,
            "turn_left": self.penalty,
            "turn_right": self.penalty,
            "accelerate": self.penalty,
            "decelerate": self.penalty,
        }

        for action in legal_actions:
            q_values[action] = 0.0

        return q_values

    def ensure_state_cached(self, state: tuple) -> dict:
        """
        Return Q-values from cache, DB, or create defaults.
        """
        if state in self.q_cache:
            return self.q_cache[state]

        q_values = self.dao.select_row_by_state(state)
        if q_values is not None:
            self.q_cache[state] = q_values
            return q_values

        legal_actions = self.get_legal_actions_from_state(state)
        q_values = self.build_default_q_values(legal_actions)

        if not self.learning_enabled:
            self.q_cache[state] = q_values.copy()
            return self.q_cache[state]

        self.dao.stage_insert_if_missing(state, q_values)
        self.q_cache[state] = q_values.copy()
        return self.q_cache[state]

    def get_q_value(self, state: tuple, action: str) -> float:
        """
        Return one Q-value for the given state and action.
        """
        q_values = self.ensure_state_cached(state)
        return q_values[action]

    def choose_action(self, state: tuple) -> str:
        """
        Choose one action with epsilon-greedy strategy.
        """
        legal_actions = self.get_legal_actions_from_state(state)

        if random.random() < self.epsilon:
            return random.choice(legal_actions)

        q_values = self.ensure_state_cached(state)
        best_actions = []
        best_value = float("-inf")

        for action in legal_actions:
            q_value = q_values[action]

            if q_value > best_value:
                best_value = q_value
                best_actions = [action]
            elif q_value == best_value:
                best_actions.append(action)

        return random.choice(best_actions)

    def learn(self, reward: float, next_state: tuple | None = None) -> None:
        """
        Learn from the previous state and action.
        """
        if not self.learning_enabled:
            return

        if self.last_state is None or self.last_action is None:
            return

        current_q_values = self.ensure_state_cached(self.last_state)
        old_value = current_q_values[self.last_action]

        if next_state is None:
            max_next = 0.0
        else:
            next_q_values = self.ensure_state_cached(next_state)
            legal_next_actions = self.get_legal_actions_from_state(next_state)
            max_next = max(
                (next_q_values[action] for action in legal_next_actions),
                default=0.0,
            )

        new_value = old_value + self.learning_rate * (
            reward + self.gamma * max_next - old_value
        )

        current_q_values[self.last_action] = new_value
        self.dao.stage_q_update(self.last_state, current_q_values)

    def play(self) -> str:
        """
        Learn from the previous move, then choose and return an action.
        """
        state = self.get_state()

        if self.last_state is not None and self.last_action is not None:
            reward = self.get_reward()
            self.learn(reward, state)

        action = self.choose_action(state)

        self.last_state = state
        self.last_action = action

        return action

    def end_episode(self, reward: float) -> None:
        """
        Apply terminal learning and reset the episode memory.
        """
        self.learn(reward, None)

        self.last_state = None
        self.last_action = None

        self.games_since_commit += 1
        if self.games_since_commit >= self.COMMIT_EVERY_GAMES:
            self.dao.flush()
            self.games_since_commit = 0

    def win(self) -> None:
        """
        Final terminal learn on win, then increment stats.
        """
        self.end_episode(self.get_reward() + self.win_reward)
        super().win()

    def lose(self) -> None:
        """
        Final terminal learn on lose, then increment stats.
        """
        self.end_episode(self.get_reward() + self.lose_reward)
        super().lose()

    def tie(self) -> None:
        """
        Final terminal learn on tie, then increment stats.
        """
        self.end_episode(0.0)
        super().tie()

    def next_epsilon(self, coefficient: float = 0.95, minimum: float = 0.05) -> float:
        """
        Decrease epsilon while keeping it above a minimum.
        """
        self.epsilon = max(minimum, self.epsilon * coefficient)
        return self.epsilon

    def force_commit(self) -> None:
        """
        Write pending DB updates immediately.
        """
        self.dao.flush()
