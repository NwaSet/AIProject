from games.pixelkart.model.kart import Kart
from games.pixelkart.const import ACTION_TO_MOVE


class Ai(Kart):
    """
    Basic PixelKart AI shell with reward settings for lap-based learning.
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

        self.color = "Red"

        self.epsilon = epsilon
        self.learning_rate = lr
        self.gamma = gamma

        self.turn_count = 0
        self.last_lap_turn = 0
        self.last_reward = 0.0

        self.q_table = {}
        self.last_state = None
        self.last_action = None

        self.step_penalty = -0.01
        self.backward_lap_penalty = -20.0
        self.win_reward = 50.0
        self.lose_reward = -50.0
        self.lap_reward_base = 100.0
        self.penalty = -10



    def get_reward(self) -> float:
        """
        Return the reward produced by the last action.
        """
        return self.last_reward

    def get_state(self):
        return (
            self.coord,
            self.direction,
            self.speed,
            *self.get_surrounding_cells()
        )

    def get_cell_value(self, row: int, col: int) -> str:
        grid = self.game.circuit.grid

        if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
            return grid[row][col]

        return "OUT"

    def get_surrounding_cells(self) -> tuple:
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

    def get_legal_actions(self) -> list:
        legal_actions =["pass_turn","turn_left","turn_right"]

        if self.speed < 2:
            legal_actions.append("accelerate")
        
        if self.speed > -1:
            legal_actions.append("decelerate")
        
        return legal_actions

    def build_default_q_values(self) ->tuple:
        legal_actions = self.get_legal_actions()
        q_values = {
            "pass_turn": self.penalty,
            "turn_left": self.penalty,
            "turn_right": self.penalty,
            "accelerate": self.penalty,
            "decelerate": self.penalty
        }
        for action in legal_actions:
            q_values[action] = 0.0
        
        return q_values


    def get_q_values(self, state: tuple, action: str):
        return self.q_table.get(state,action),0.0)


    def choose_action(self, state: tuple) -> str:
        legal_actions = self.get_legal_actions()

        if random.random() < self.epsilon:
            return random.choice(legal_actions)

        best_actions = []
        best_value = float("-inf")

        for action in legal_actions:
            q_value = self.get_q_value(state, action)

            if q_value > best_value:
                best_value = q_value
                best_actions = [action]
            elif q_value == best_value:
                best_actions.append(action)

        return random.choice(best_actions)

    def learn(self, reward: float, next_state: tuple | None = None) -> None:
        if self.last_state is None or self.last_action is None:
            return

        old_value = self.get_q_value(self.last_state, self.last_action)

        if next_state is None:
            max_next = 0.0
        else:
            legal_next_actions = self.get_legal_actions()
            max_next = max(
                (self.get_q_value(next_state, action) for action in legal_next_actions),
                default=0.0,
            )

        new_value = old_value + self.learning_rate * (
            reward + self.gamma * max_next - old_value
        )

        self.q_table[(self.last_state, self.last_action)] = new_value
    
    def play(self) -> str:
        state = self.get_state()

        if self.last_state is not None and self.last_action is not None:
            reward = self.get_reward()
            self.learn(reward, state)

        action = self.choose_action(state)

        self.last_state = state
        self.last_action = action

        return action
