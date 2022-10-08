from random import *

import pickle
from environment.metrics import ActionMoves


class Agent:
    def __init__(self, env, alpha=1, gamma=0.8, cooling_rate=0.999):
        self.__temperature = 0
        self.__score = 0
        self.__state = env.state
        self.__qtable = {}
        """
        Should we init the qtable with all the possible states? 
        """
        self.__env = env
        self.__alpha = alpha
        self.__gamma = gamma
        self.__history = []
        self.__cooling_rate = cooling_rate
        self.reset(False)

    def reset(self, store_history=True):
        if store_history:
            self.__history.append(self.__score)
        self.__env.reset()
        self.__score = 0
        self.__temperature = 0

    def heat(self):
        self.__temperature = 1

    def best_action(self):
        if random() < self.__temperature:
            self.__temperature *= self.__cooling_rate
            return choice(ActionMoves().list())
        else:
            if self.__state not in self.__qtable:
                self.__qtable[self.__state] = {
                    ActionMoves.N: 0,
                    ActionMoves.E: 0,
                    ActionMoves.S: 0,
                    ActionMoves.O: 0
                }
            q = self.__qtable[self.__state]
            return max(q, key=q.get)

    def step(self):
        action = self.best_action()

        state, reward = self.__env.do(action)
        if state not in self.__qtable:
            self.__qtable[state] = {
                ActionMoves.N: 0,
                ActionMoves.E: 0,
                ActionMoves.S: 0,
                ActionMoves.O: 0
            }
        maxQ = max(self.__qtable[state].values())
        delta = self.__alpha * (reward + self.__gamma *
                                maxQ - self.__qtable[self.__state][action])
        self.__qtable[self.__state][action] += delta

        self.__state = state
        self.__score += reward
        return action, reward

    def load(self, filename):
        with open(filename, 'rb') as file:
            self.__qtable, self.__history = pickle.load(file)

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump((self.__qtable, self.__history), file)

    @property
    def state(self):
        return self.__state

    @property
    def score(self):
        return self.__score

    @property
    def environment(self):
        return self.__env

    @property
    def history(self):
        return self.__history

    @property
    def temperature(self):
        return self.__temperature

    def __repr__(self):
        res = f'Agent {self.__state}\n'
        res += str(self.__qtable)
        return res
