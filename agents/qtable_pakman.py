from copy import deepcopy
from random import *

import pickle
from core_game.actions import Action
from core_game.pakman import Pakman
from core_game.position import Position
from environment.environment import Environment
from environment.state import State


class QtablePakman(Pakman):
    @property
    def state(self) -> State:
        return self.__state

    @property
    def score(self) -> float:
        return self.__score

    @property
    def history(self) -> list[float]:
        return self.__history

    @property
    def temperature(self) -> float:
        return self.__temperature

    def __init__(self, initial_position: Position, initial_state: State, env: Environment, qtable=None, alpha=1, gamma=0.8, cooling_rate=0.999) -> None:
        super().__init__(initial_position)

        self.__temperature = 0.0
        self.__score = 0.0
        self.__env = env
        self.__initial_state = initial_state
        self.__state = deepcopy(initial_state)
        self.qtable: dict[
            State, 
            dict[Action, float]
        ] = qtable if qtable != None else {}

        self.__alpha = alpha
        self.__gamma = gamma
        self.__history = []
        self.__cooling_rate = cooling_rate
        # self.reset(False)

    def reset(self, store_history=True) -> None:
        if store_history:
            self.__history.append(self.__score)
        self.__state = deepcopy(self.__initial_state)
        self.__score = 0.0
        self.__temperature = 0.0

    def heat(self) -> None:
        self.__temperature = 1.0

    def _best_action(self) -> Action:
        if random() < self.__temperature:
            self.__temperature *= self.__cooling_rate
            return choice(Action.as_list())

        actions = self.__qtable_get_or_create(self.__state)
        return max(actions, key=actions.get)

    def step(self) -> tuple[Action, float]:
        action = self._best_action()

        self._position, state, reward, isDead = self.__env.do(action, self.__state, self.position)
        maxQ = max(self.__qtable_get_or_create(state).values())
        delta = self.__alpha * (reward + self.__gamma * maxQ - self.__qtable_get_or_create(self.__state)[action])
        
        self.qtable[self.__state][action] += delta

        self.__state = state
        self.__score += reward

        if isDead:
            self.die()
        else:
            self._direction = action.to_direction()
        print(self.qtable[self.__state])
        print(f"chosen action is {action}")
        return action, reward 

    def __qtable_get_or_create(self, state: State) -> dict[Action, float]:
        return self.qtable.setdefault(
            state,
            { k: 0.0 for k in Action.as_list() }
        )

    def load(self, filename = "qtable_pakman.dump") -> None:
        with open(filename, 'rb') as file:
            self.qtable, self.__history = pickle.load(file)

    def save(self, filename = "qtable_pakman.dump") -> None:
        with open(filename, 'wb') as file:
            pickle.dump((self.qtable, self.__history), file)

    def __repr__(self) -> str:
        res = f'Agent {self.__state}\n'
        res += str(self.qtable)
        return res
