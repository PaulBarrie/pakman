from agents.qtable_pakman import QtablePakman
from agents.type import ModelType
from core_game.pakman import Pakman
from environment.environment import Environment
from environment.state import State


class PakmanGame:
    @property
    def agent(self):
        return self.__agent

    @property
    def environment(self):
        return self.__environment

    @property
    def iteration(self):
        return self.__iteration

    def __init__(self, environment: Environment, agent: Pakman) -> None:
        self.__agent = agent
        self.__agent_type = agent.__class__
        self.__environment = environment
        self.__current_agent_index = 0
        self.__iteration = 0

    def update(self):
        if self.__current_agent_index == 1:
            blinky = self.__environment.blinky
            blinky.step(self.__environment.walls, self.__agent)

        elif self.__current_agent_index == 2:
            inky = self.__environment.inky
            inky.step(self.__environment.walls, self.__agent)

        elif self.__current_agent_index == 3:
            pinky = self.__environment.pinky
            pinky.step(self.__environment.walls, self.__agent)

        elif self.__current_agent_index == 4:
            clyde = self.__environment.clyde
            clyde.step(self.__environment.walls, self.__agent)

        else:
            print(f"Agent lives: {self.__agent.lives}")
            if self.__agent.lives > 0 and len(self.__environment.gums) > 0:
                self.__agent.step()
            else:
                self.reset()

        self.__current_agent_index = (self.__current_agent_index + 1) % 5

    def reset(self):
        self.__iteration += 1
        self.__environment = Environment.from_str_map(self.__environment.str_map)
        initial_state = State.compute_state(
            self.__environment.ghost_positions,
            self.__environment.initial_pakman_position,
            self.__environment.gums,
            self.__environment.walls
        )
        print("RESET")
        self.__agent.__class__ = self.__agent_type
        self.__agent = self.__agent.reset(self.__environment.initial_pakman_position, initial_state, self.__environment,
                                          qtable=self.__agent.qtable, history=self.__agent.history)
        print(self.__agent)
        print(f"Agent lives: {self.__agent.lives}")