import random
from .player import Player
from games.Cubee.model.cubee_model import GameModel
from games.Cubee.DAO.dao import Dao

# add self.reward en cas de retour sur une case déja à nous ?
# faire la fonction to_dto que j'aurais besoin dans le dao
# le nom du dao devra etre les paramètre pour avoir plus facile à les trier 


class IA(Player):
    def __init__(self, id: int, name: str, game: object = None) -> None:
        super().__init__(id, name, game)
        self.color = "gray"

        self.lose_reward = -10
        self.win_reward = +10
        self.penalty = -5
        self.take_cell = 1

        self.epsilon = 0.9
        self.learning_rate = 0.01
        self.gamma = 1

        self.game = game

        self.dao = Dao(self.name)

    def move_to_string(self, move):
        return {(0, -1): "up", (0, 1): "down", (-1, 0): "left", (1, 0): "right"}[move]

    def string_to_move(self, action):
        return {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}[action]

    def init_state(self, state, legal_moves):

        data = {**state, "up": -5, "down": -5, "left": -5, "right": -5}
        for move in legal_moves:
            data[move] = 0

        self.dao.add_row(data)
        return data

    def choose_move(self, state):
        choice = None
        legal_moves = self.game.legal_move()

        actions = self.dao.select_row_by_dto(state)
        if actions is None:
            actions = self.init_state(state, legal_moves)
        legal_action = {
            self.move_to_string(move): actions[self.move_to_string(move)]
            for move in legal_moves
        }

        if random.random() < self.epsilon:
            choice = random.choice(list(legal_action.keys()))
        else:
            max_val = max(legal_action.values())
            best_moves = [k for k, v in legal_action.items() if v == max_val]
            choice = random.choice(best_moves)
        return choice

    def compute_reward(self, info):

        reward = self.penalty

        if info.get("took_case"):
            reward += self.take_cell

        if info.get("win"):
            reward += self.win_reward

        if info.get("lose"):
            reward += self.lose_reward

        return reward

    def q_function(self, state, action, reward, next_state):
        # attention tu fais update mais il est possible qu'il faut faire add_row si elle existe pas
        current = self.dao.select_row_by_dto(state)
        next_action = self.dao.select_row_by_dto(next_state)

        if next_action is None:
            max_next = 0
        else:
            max_next = max(next_action.values())

        old_value = current[action]

        new_value = old_value + self.learning_rate * (reward + self.gamma*max_next - old_value)
        current[action] = new_value

        self.dao.update_row(current)

    def play_turn(self):
        state = self.game.get_state_dto()

        action = self.choose_move(state, self.game.legal_move())

        move = self.string_to_move(action)
        info = self.game.play_ai_step(move)

        reward = self.compute_reward(info)

        next_state = self.game.get_state_dto()

        self.q_function(state, action, reward, next_state)

    def next_epsilon(self, coefficient: float = 0.95, minimum: float = 0.05) -> float:
        """
        Decrease epsilon while keeping it above a minimum value.
        """
        self.epsilon = max(minimum, self.epsilon * coefficient)
        return self.epsilon
