from __future__ import annotations
from core_game.actions import Action
from core_game.position import Position
from metrics import *
from state import State

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

    # @property
    # def start(self):
    #     return self.__init_position

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
    def pakman_position(self) -> Position:
        return self.__pakman_position

    @property
    def ghost_positions(self) -> list[Position]:
        return self.__ghost_positions

    @property
    def gums(self) -> list[Position]:
        return self.__gums

    def __init__(
        self, width: int, 
        height: int, 
        gums: list[Position], 
        walls: list[Position], 
        pakman_position: Position, 
        ghost_positions: dict[str, Position], 
        initial_state: State
    ) -> None:

        self.__width = width
        self.__height = height
        self.__gums = gums
        self.__walls = walls
        self.__initial_pakman_position = pakman_position
        self.__pakman_position = pakman_position
        self.__ghost_positions = ghost_positions
        self.__state = initial_state

    @staticmethod
    def from_str_map(str_map: str) -> Environment:
        row = 0
        col = 0
        gums = []
        walls = []
        ghosts = []
        pakman = None

        for line in str_map.strip().split('\n'):
            col = 0
            for item in line:
                if item == MAP_GUM:
                    gums.append(Position(row, col))
                elif item == MAP_WALL:
                    walls.append(Position(row, col))
                elif item in MAP_GHOSTS:
                    ghosts.append(Position(row, col))
                elif item == MAP_PACMAN:
                    pakman = Position(row, col)

                col += 1
            row += 1

        if pakman is None or ghosts.count() == 0:
            raise ValueError("Missing Pakman and/or ghost(s)")

        return Environment(col, row, gums, walls, pakman, ghosts)

    def do(self, action: Action, state=None) -> tuple[Position, State, float, bool]:
        next_position = self.__pakman_position.apply_action(action)
        next_state = State.compute_state(self.__ghost_positions, next_position, self.__gums, self.__walls)

        if next_position in self.__ghosts:
            self.__pakman_position = self.__initial_pakman_position
            reset_state = State.compute_state(self.__ghost_positions, self.__pakman_position, self.__gums, self.__walls)
            return (self.__initial_pakman_position, reset_state, REWARD_GHOST, True)

        if next_position in self.__walls:
            return (self.__pakman_position, state, REWARD_WALL, False)

        if next_position in self.__gums:
            self.__gums.remove(next_position)

        self.__pakman_position = next_position
        return (next_position, next_state, REWARD_DEFAULT, False)

    def update_ghost_positions(self, ghost_positions: dict[str, Position]) -> None:
        self.__ghost_positions = ghost_positions
            
    def is_wall(self, coordinates: tuple[int, int]) -> bool:
        return coordinates in self.__walls

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
