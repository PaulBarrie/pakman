from agents.qtable_pakman import QtablePakman
from core_game.pakman import Pakman

from environment.environment import Environment
from environment.state import State
from pakman_game import PakmanGame


class PakmanWindowless():
    def __init__(self, environment: Environment, agent: Pakman):
        self.__game = PakmanGame(environment, agent)

    def update(self):
        self.__game.update()

    def reset(self):
        self.__game.reset()
