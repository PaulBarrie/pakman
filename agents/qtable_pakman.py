from copy import deepcopy
from random import *

import pickle
from typing import Dict, Union

import numpy as np

from core_game.actions import Action
from core_game.pakman import Pakman
from core_game.position import Position
from environment.environment import Environment
from environment.state import State, DQLearnState


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

    @property
    def environment(self) -> Environment:
        return self.__environment

    @property
    def qtable(self):
        return self.__qtable

    @property
    def history(self):
        return self.__history

    def __init__(self, initial_position: Position, initial_state: [State, DQLearnState], environment: Environment, qtable=None, history=None,
                 alpha=1, gamma=0.8, cooling_rate=0.999) -> None:
        super().__init__(initial_position)

        self.__temperature = 0.0
        self.__score = 0.0
        self.__environment = environment
        self.__initial_state = initial_state
        self.__state = deepcopy(initial_state)
        self.__qtable: dict[
            State,
            dict[Action, float]
        ] = qtable if qtable is not None else {}

        self.__alpha = alpha
        self.__gamma = gamma
        self.__history = history if history is not None else []
        self.__cooling_rate = cooling_rate

    def heat(self) -> None:
        self.__temperature = 1.0

    def _best_action(self) -> Action:
        if random() < self.__temperature:
            self.__temperature *= self.__cooling_rate
            return choice(Action.as_list())

        actions = self.__qtable_get_or_create(self.__state)
        return max(actions, key=actions.get)

    def update_environment_and_agent(self, action: Action, dry=False) -> tuple[float, bool]:
        self._position, state, reward, isDead = self.__environment.do(action, self.__state, self.position)
        maxQ = max(self.__qtable_get_or_create(state).values())
        delta = self.__alpha * (reward + self.__gamma * maxQ - self.__qtable_get_or_create(self.__state)[action])

        self.__qtable[self.__state][action] += delta
        self.__state = state
        print(reward)
        self.__score += reward

        return reward, isDead

    def update_q_table(self, state: State, action: Action, reward: float) -> dict[State, dict[Action, float]]:
        maxQ = max(self.__qtable_get_or_create(state).values())
        delta = self.__alpha * (reward + self.__gamma * maxQ - self.__qtable_get_or_create(self.__state)[action])
        qtable = deepcopy(self.__qtable)
        qtable[state][action] += delta
        return qtable

    def dry_update_environment_and_agent(self, action: Action) -> tuple[float, bool]:
        position, state, reward, isDead = self.__environment.do_dry(action, self.position)
        qtable = self.update_q_table(self.__state, action, reward, state)

        return qtable[state][action], isDead

    def get_output_reward(self) -> np.array:
        action_list = Action.as_list()
        res = np.zeros(shape=(len(action_list), 1))
        for action in range(len(action_list)):
            next_position, next_state, reward, isDead = self.__environment.do_dry(action_list[action], super().position)
            res[action] = reward
        return res

    def get_qtable_reward(self) -> np.array:
        action_list = Action.as_list()
        res = np.zeros(shape=(len(action_list), 1))
        for action in range(len(action_list)):
            next_position, next_state, reward, isDead = self.__environment.do_dry(action_list[action], super().position)
            res[action] = self.__qtable_get_or_create(self.__state)[action_list[action]]
        return res

    def step(self, action=None) -> tuple[Action, float]:
        if action is None:
            action = self._best_action()
        reward, isDead = self.update_environment_and_agent(action)

        if isDead:
            self.die()
        else:
            self._direction = action.to_direction()
        # print(self.__qtable[self.__state])
        print(f"chosen action is {action}")
        self.__history.append(self.__score)
        return action, reward

    def __qtable_get_or_create(self, state: State) -> dict[Action, float]:
        return self.__qtable.setdefault(
            state,
            {k: 0.0 for k in Action.as_list()}
        )

    def reset(self, initial_position: Position, initial_state: State, environment: Environment,
              qtable=None, history=None):
        super().reset_pakman(initial_position)
        self.__state = initial_state
        self.__environment = environment
        self.__qtable = qtable if qtable is not None else {}
        self.__history = history if history is not None else []
        return self

    def load(self, filename="qtable_pakman.dump") -> None:
        with open(filename, 'rb') as file:
            self.__qtable, self.__history = pickle.load(file)

    def save(self, filename="qtable_pakman.dump") -> None:
        with open(filename, 'wb') as file:
            pickle.dump((self.__qtable, self.__history), file)

    def __repr__(self) -> str:
        res = f'Agent {self.__state}\n'
        res += str(self.__qtable)
        return res


