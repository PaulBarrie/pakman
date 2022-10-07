from __future__ import annotations
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

REWARD_GUM = 1
REWARD_DEFAULT = -1
NB_STATES = 2 ** 4 * 2 ** 4 * 8 * 4
REWARD_GHOST = -NB_STATES
REWARD_WALL = -2 * REWARD_GHOST


class Environment:
    @property
    def state(self) -> State:
        return self.__state

    @property
    def pakman_initial_position(self) -> Position:
        return self.__pakman_initial_position

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

    def __init__(
        self, width: int, 
        height: int, 
        gums: list[Position], 
        walls: list[Position], 
        pakman_position: Position, 
        blinky: Ghost,
        inky: Ghost,
        pinky: Ghost,
        clyde: Ghost
    ) -> None:

        self.__width = width
        self.__height = height
        self.__gums = gums
        self.__walls = walls
        self.__initial_pakman_position = pakman_position
        self.__blinky = blinky
        self.__inky = inky
        self.__pinky = pinky
        self.__clyde = clyde

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

        for line in str_map.strip().split('\n'):
            col = 0
            for item in line:
                if item == MAP_GUM:
                    gums.append(Position(row, col))
                elif item == MAP_WALL:
                    walls.append(Position(row, col))
                elif item == MAP_BLINKY:
                    blinky = GhostFactory.spawn_blinky(Position(row, col))
                elif item == MAP_INKY:
                    inky = GhostFactory.spawn_inky(Position(row, col))
                elif item == MAP_PINKY:
                    pinky = GhostFactory.spawn_pinky(Position(row, col))
                elif item == MAP_CLYDE:
                    clyde = GhostFactory.spawn_blinky(Position(row, col))
                elif item == MAP_PACMAN:
                    pakman_position = Position(row, col)

                col += 1
            row += 1

        if pakman_position is None or \
            (blinky is None and inky is None and pinky is None and clyde is None):
            raise ValueError("Missing Pakman and/or ghost(s)")

        return Environment(col, row, gums, walls, pakman_position, blinky, inky, pinky, clyde)

    def do(self, action: Action, state: State, position: Position) -> tuple[Position, State, float, bool]:
        next_position = position.apply_action(action)
        next_state = State.compute_state(self.ghost_positions, next_position, self.__gums, self.__walls)

        if next_position in self.__ghosts:
            reset_state = State.compute_state(self.ghost_positions, position, self.__gums, self.__walls)
            return (self.__initial_pakman_position, reset_state, REWARD_GHOST, True)

        if next_position in self.__walls:
            return (position, state, REWARD_WALL, False)

        if next_position in self.__gums:
            self.__gums.remove(next_position)

        return (next_position, next_state, REWARD_DEFAULT, False)

    """
    def print(self, agent):
        res = ''
        for row in range(self.__rows):
            for col in range(self.__cols):
                state = (row, col)
                if state == agent.state:
                    res += 'A'
                else:
                    res += self.__states[(row, col)]

            res += '\n'
        print(res)
    """
