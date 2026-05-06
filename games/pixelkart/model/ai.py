from games.pixelkart.model.kart import Kart


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

        self.step_penalty = -0.01
        self.backward_lap_penalty = -20.0
        self.win_reward = 50.0
        self.lose_reward = -50.0
        self.lap_reward_base = 100.0



    def get_reward(self) -> float:
        """
        Return the reward produced by the last action.
        """
        return self.last_reward

    def get_state(self):
        cell = self.get_surrounding_cells()
        return (
            self.coord,
            self.direction,
            self.speed,
            *cell
        )

    def get_cell_value(self, row: int, col: int) -> str:
        grid = self.game.circuit.grid

        if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
            return grid[row][col]

        return "OUT"

    def get_surrounding_cells(self) -> tuple[str, ...]:
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

    def get_legal_actions(self):
        legal_actions =["pass_turn","turn_left","turn_right"]

        if self.speed < 2:
            legal_actions.append("accelerate")
        
        if self.speed > -1:
            legal_actions.append("decelerate")
        
        return legal_actions

    def get_q_value(self):
