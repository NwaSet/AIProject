from .player import *
import json

class AI(Player) :

    """
    class AI

    it is an AI player that will learn by renforcement.
    V(s) <- V(s) + lr * (V(s') - V(s))
    """

    def __init__(
            self,
            name : str,
            game : object = None
            ) -> None :
        
        """
        function that initiate all attributs:

        lose_Reward     : the reward given after a lose
        win_reward      : the reward given after a win
        epsilon         : say if the choice of the AI is random or exploit, value between 0 - 1
        learning_rate   : how fast the AI learn 
        history         : list of all tuple of history : (previous_state, state)
        previous_state  : previous state in the game
        self.v_function : say if the state is good or not. value between -1 - 1
        """

        super().__init__(name, game)

        self.lose_reward = -1
        self.win_reward = +1

        self.epsilon = 0.9
        self.learning_rate = 0.01
        self.history = []
        self.previous_state = None

        self.v_fuction = {"lose": self.lose_reward, "win": self.win_reward}


    def legal_actions(self) -> list[int] :
        """
        Return a list of legal actions according to the remaining number of sticks.
        max 3 min 1
        """

        max_take = min(3, self.game.nb_stick)
        return list(range(1, max_take + 1))


    def get_value(
            self,
            state: object
            ) -> float :
        """
        Return V(state), creating intermediate states at 0 when unknown.
        """

        if state not in self.v_fuction :
            self.v_fuction[state] = 0.0
        return self.v_fuction[state]


    def explore(self) -> int :
        """
        Random action in the legal actions.
        """

        return random.choice(self.legal_actions())


    def exploit(self) -> int :
        """
        Choose the action that minimizes the value of the opponent next state.
        """

        actions = self.legal_actions()
        best_actions = []
        min_opponent_value = 10000

        for action in actions :
            opponent_state = self.game.nb_stick - action
            opponent_value = self.get_value(opponent_state)

            if opponent_value < min_opponent_value :
                min_opponent_value = opponent_value
                best_actions = [action]
            elif opponent_value == min_opponent_value :
                best_actions.append(action)

        return random.choice(best_actions)


    def play(self) -> int :
        """
        save the previous state of the game, 
        make a move (explore or exploit)
        update previous state
        """

        current_state = self.game.nb_stick if self.game is not None else None

        if self.previous_state is not None and current_state is not None :
            self.history.append((self.previous_state, current_state))

        if random.random() < self.epsilon:
            action = self.explore()
        else:
            action = self.exploit()

        self.previous_state = current_state
        return action


    def win(self) -> None :
        """
        Register win and final transition, then train.
        """

        super().win()
        if self.previous_state is not None :
            self.history.append((self.previous_state, "win"))
        self.previous_state = None
        self.train()


    def lose(self) -> None :
        """
        Register loss and final transition, then train.
        """

        super().lose()
        if self.previous_state is not None :
            self.history.append((self.previous_state, "lose"))
        self.previous_state = None
        self.train()


    def train(self) -> None :
        """
        Backward TD update: V(s) <- V(s) + lr * (V(s') - V(s))
        """

        for state, next_state in reversed(self.history):
            state_value = self.get_value(state)
            next_state_value = self.get_value(next_state)
            self.v_fuction[state] = state_value + self.learning_rate * (next_state_value - state_value)

        self.history.clear()


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


    def upload(self) -> None :
        """
        create or overwrite a json file in the data folder with all data needed for the AI
        """

        with open(f"mikado/player/data/{self.name}Data.json", "w") as file :
            data = {
                "v_function": self.v_fuction,
                "epsilon": self.epsilon
            }
            json.dump(data, file)
    

    def download(
            self,
            file_name : str
            ) -> None :
        """
        read the json fil with the file_name and copy all data needed in self.
        """

        with open(f"mikado/player/data/{file_name}Data.json", "r") as file :
            data = json.load(file)

            self.v_fuction = data.get("v_function")
            self.epsilon = data.get("epsilon")
