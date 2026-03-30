import random
from games.cubee.player.player import *
from games.cubee.dao.dao import *


class Ia(Player) :

    """
    AI player using Q-learning.

    Q(s, a) <- Q(s, a) + lr * (reward + gamma * max(Q(s', .)) - Q(s, a))
    """

    def __init__(
            self,
            id: int,
            name: str,
            game: object = None,
            epsilon : float= 0.9,
            lr : float = 0.1,
            gamma : float = 0.8
            ) -> None :
        """
        initialize the Ai : 

        Args :
        id : id of hte player
        name : name of the ai
        game : game model where the player is playing
        epsilon : represente if the play chose a randome move or a good move
        lr : how fast the ai will learn
        gamma : the importance of the instant move 
        """

        super().__init__(id, name, game)
        self.color = "gray"

        self.lose_reward = -5
        self.win_reward = 5
        self.penalty = -0.1
        self.take_cell = 1

        self.epsilon = epsilon
        self.learning_rate = lr
        self.gamma = gamma

        self.dao = Dao(f"ia_lr{self.learning_rate}_g{self.gamma}")

        self.last_state = None
        self.last_action = None

    def move_to_string(
            self,
            move: tuple[int, int]
            ) -> str :
        """
        return the move made as a string
        need a tuple as action
        """

        return {
            (0, -1): "up",
            (0, 1): "down",
            (-1, 0): "left",
            (1, 0): "right",
        }[move]

    def string_to_move(
            self,
            action: str
            ) -> tuple[int, int] :
        """
        return the move made as a tuple
        need a string as action
        """

        return {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }[action]


    def legal_actions(self) -> list[str] :
        """
        Return legal actions as strings.
        """

        return [self.move_to_string(move) for move in self.game.legal_move()]


    def init_state(
            self,
            state: dict
            ) -> dict :
        """
        Create the state in DAO if it does not exist.
        Legal actions start at 0.
        Illegal actions start at penalty.
        """

        legal_actions = self.legal_actions()

        data = {
            "current_player": state["current_player"],
            "player1_coord": state["player1_coord"],
            "player2_coord": state["player2_coord"],
            "grid": state["grid"],
            "grid_size": state["grid_size"],
            "up": self.penalty,
            "down": self.penalty,
            "left": self.penalty,
            "right": self.penalty,
        }

        for action in legal_actions :
            data[action] = 0.0

        self.dao.add_row(data)

        return {
            "up": data["up"],
            "down": data["down"],
            "left": data["left"],
            "right": data["right"],
        }

    def get_q_values(
            self,
            state: dict
            ) -> dict:
        """
        Return Q-values of a state.
        Create the state if unknown.
        """

        q_values = self.dao.select_row_by_dto(state)

        if q_values is None :
            q_values = self.init_state(state)

        return q_values


    def explore(self) -> str :
        """
        Choose a random legal action.
        Save current state/action for future Q update.
        """

        state = self.game.get_state_dto()
        self.get_q_values(state)

        action = random.choice(self.legal_actions())

        self.last_state = state
        self.last_action = action

        return action


    def exploit(self) -> str :
        """
        Choose the best legal action according to Q-values.
        Save current state/action for future Q update.
        """

        state = self.game.get_state_dto()
        q_values = self.get_q_values(state)
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

        action = random.choice(best_actions)

        self.last_state = state
        self.last_action = action

        return action


    def compute_reward(
            self,
            info: dict
            ) -> float :
        """
        Compute reward after the move.
        """

        reward = self.penalty

        if info.get("took_case") :
            reward += self.take_cell

        if info.get("win") :
            reward += self.win_reward

        if info.get("lose") :
            reward += self.lose_reward

        return reward


    def q_function(
            self,
            state: dict,
            action: str,
            reward: float,
            next_state: dict
            ) -> None :
        """
        Apply Q-learning update.
        """

        current_q_values = self.get_q_values(state)
        next_q_values = self.get_q_values(next_state)

        old_value = current_q_values[action]
        max_next = max(next_q_values[a] for a in ["up", "down", "left", "right"])

        new_value = old_value + self.learning_rate * (
            reward + self.gamma * max_next - old_value
        )

        current_q_values[action] = new_value

        self.dao.select_row_by_dto(state)
        self.dao.update_row(current_q_values)


    def update_after_move(
            self,
            info: dict
            ) -> None:
        """
        Must be called by the GameModel after the move has been applied.
        """

        if self.last_state is None or self.last_action is None :
            return

        reward = self.compute_reward(info)
        next_state = self.game.get_state_dto()

        self.q_function(self.last_state, self.last_action, reward, next_state)

        self.last_state = None
        self.last_action = None


    def play(self) -> tuple[int, int] :
        """
        Choose a move with epsilon-greedy and return the move.
        The move is NOT applied here.
        """

        if random.random() < self.epsilon :
            action = self.explore()
        else :
            action = self.exploit()

        return self.string_to_move(action)


    def next_epsilon(
            self,
            coefficient: float = 0.95,
            minimum: float = 0.05
            ) -> float :
        """
        Decrease epsilon while keeping it above a minimum value.
        """

        self.epsilon = max(minimum, self.epsilon * coefficient)
        return self.epsilon