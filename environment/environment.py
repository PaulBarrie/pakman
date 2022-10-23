from __future__ import annotations

import numpy as np

from core_game.actions import Action
from core_game.ghost import Ghost
from core_game.ghost_factory import GhostFactory
from core_game.position import Position
from environment.state import State
from environment.metrics import *

MAP_WALL = '#'
MAP_GUM = '.'
MAP_PACMAN = 'P'
MAP_EMPTY = ' '
MAP_INKY = 'I'
MAP_BLINKY = 'B'
MAP_CLYDE = 'C'
MAP_PINKY = 'R'
MAP_GHOSTS = [MAP_INKY, MAP_BLINKY, MAP_CLYDE, MAP_PINKY]
MAP_GHOST = 'G'
LONG_RANGE_RADAR_STATES = 2 ** 4 * 4
SHORT_RANGE_RADAR_STATES = 2 ** 4
POSITION_STATES = 21 * 28
NB_STATES = (LONG_RANGE_RADAR_STATES * SHORT_RANGE_RADAR_STATES * SHORT_RANGE_RADAR_STATES * POSITION_STATES)
REWARD_DEFAULT = 0
REWARD_GHOST = -NB_STATES
REWARD_WALL = REWARD_GHOST / 10
REWARD_GUM = 100


STATE_NUMERIC_ENCODING = {
    MAP_EMPTY: 0,
    MAP_GUM: 1,
    MAP_GHOST: 2,
    MAP_PACMAN: 3,
    MAP_WALL: 4,
}


class Environment:
    @property
    def state(self) -> State:
        return self.__state

    @property
    def initial_pakman_position(self) -> Position:
        return self.__initial_pakman_position

    @property
    def blinky(self) -> Ghost:
        return self.__blinky

    @property
    def inky(self) -> Ghost:
        return self.__inky

    @property
    def pinky(self) -> Ghost:
        return self.__pinky

    @property
    def clyde(self) -> Ghost:
        return self.__clyde

    @property
    def height(self) -> int:
        return self.__height

    @property
    def width(self) -> int:
        return self.__width

    @property
    def walls(self) -> list[Position]:
        return self.__walls

    @property
    def gums(self) -> list[Position]:
        return self.__gums

    @property
    def ghost_positions(self) -> list[Position]:
        return [
            self.__blinky.position,
            self.__inky.position,
            self.__pinky.position,
            self.__clyde.position
        ]
    @property
    def data_environment(self) -> np.ndarray:
        return self.__data_environment

    def __init__(
        self, width: int, 
        height: int, 
        gums: list[Position], 
        walls: list[Position], 
        pakman_position: Position, 
        blinky: Ghost,
        inky: Ghost,
        pinky: Ghost,
        clyde: Ghost,
        str_map: str,
        data_environment: np.ndarray
    ) -> None:

        self.__width = width
        self.__height = height
        self.__gums = gums
        self.__gum_reward = len(gums)
        self.__walls = walls
        self.__initial_pakman_position = pakman_position
        self.__blinky = blinky
        self.__inky = inky
        self.__pinky = pinky
        self.__clyde = clyde
        self.__str_map = str_map
        self.__data_environment = data_environment
        
    @staticmethod
    def from_str_map(str_map: str) -> Environment:
        row = 0
        col = 0
        gums = []
        walls = []
        pakman_position = None
        blinky = None
        inky = None
        pinky = None
        clyde = None

        data_env = np.array()

        for line in str_map.strip().split('\n'):
            line = []
            col = 0
            for item in line:
                if item == MAP_GUM:
                    gums.append(Position(row, col))
                    line.append(REWARD_GUM)
                elif item == MAP_WALL:
                    walls.append(Position(row, col))
                    line.append(REWARD_WALL)
                elif item == MAP_BLINKY:
                    blinky = GhostFactory.spawn_blinky(Position(row, col))
                    line.append(REWARD_GHOST)
                elif item == MAP_INKY:
                    inky = GhostFactory.spawn_inky(Position(row, col))
                    line.append(REWARD_GHOST)
                elif item == MAP_PINKY:
                    pinky = GhostFactory.spawn_pinky(Position(row, col))
                    line.append(REWARD_GHOST)
                elif item == MAP_CLYDE:
                    clyde = GhostFactory.spawn_blinky(Position(row, col))
                    line.append(REWARD_GHOST)
                elif item == MAP_PACMAN:
                    pakman_position = Position(row, col)
                    line.append(REWARD_DEFAULT)
                col += 1
            data_env.append(line)
            line = []
            row += 1

        if pakman_position is None or \
                (blinky is None and inky is None and pinky is None and clyde is None):
            raise ValueError("Missing Pakman and/or ghost(s)")

        return Environment(col, row, gums, walls, pakman_position, blinky, inky, pinky, clyde, str_map, data_env)

    def do(self, action: Action, state: State, position: Position) -> tuple[Position, State, float, bool]:
        next_position = position.apply_action(action)
        next_state = State.compute_state(self.ghost_positions, next_position, self.__gums, self.__walls)

        if next_position in self.ghost_positions:
            reset_state = State.compute_state(self.ghost_positions, position, self.__gums, self.__walls)
            return self.__initial_pakman_position, reset_state, REWARD_GHOST, True

        if next_position in self.__walls:
            return position, state, REWARD_WALL, False

        if next_position in self.__gums:
            self.__gums.remove(next_position)
            return next_position, next_state, self.gum_reward(), False

        return next_position, next_state, REWARD_DEFAULT, False

    def do_dry(self, action: Action, position: Position) -> tuple[Position, State, float, bool]:
        next_position = position.apply_action(action)
        next_state = State.compute_state(self.ghost_positions, next_position, self.__gums, self.__walls)

        if next_position in self.ghost_positions:
            return self.__initial_pakman_position, next_state, REWARD_GHOST, True

        if next_position in self.__walls:
            return position, next_state, REWARD_WALL, False

        if next_position in self.__gums:
            return next_position, next_state, self.gum_reward(), False

        return next_position, next_state, REWARD_DEFAULT, False

    def gum_reward(self):
        remaining_gums = len(self.gums)
        if remaining_gums == 0:
            return NB_STATES
        return self.__total_gums - len(self.__gums)

    def as_multinomial_array(self):
        res = np.zeros(shape=(self.__height, self.__width))
        for gum in self.__gums:
            res[gum.row, gum.column] = STATE_NUMERIC_ENCODING[MAP_GUM]
        for wall in self.__walls:
            res[wall.row, wall.column] = STATE_NUMERIC_ENCODING[MAP_WALL]
        for ghost in self.ghost_positions:
            res[ghost.row, ghost.column] = STATE_NUMERIC_ENCODING[MAP_GHOST]
        res[self.__initial_pakman_position.row, self.__initial_pakman_position.column] = STATE_NUMERIC_ENCODING[MAP_PACMAN]

        return res

    def as_reward_array(self):
        res = np.zeros(shape=(self.__height, self.__width))
        for gum in self.__gums:
            res[gum.row, gum.column] = REWARD_GUM
        for wall in self.__walls:
            res[wall.row, wall.column] = REWARD_WALL
        for ghost in self.ghost_positions:
            res[ghost.row, ghost.column] = REWARD_GHOST
        res[self.__initial_pakman_position.row, self.__initial_pakman_position.column] = REWARD_DEFAULT

        return res
