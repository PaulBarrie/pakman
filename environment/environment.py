from random import random
import numpy as np
from radars import ShortRangeRadar, GhostRadar
MAP_WALL = '#'
MAP_GUM = '.'
MAP_PACMAN = 'P'
MAP_EMPTY = ' '
MAP_INKY = 'I'
MAP_BLINKY = 'B'
MAP_CLYDE = 'C'
MAP_PINKY = 'P'
MAP_GHOSTS = [MAP_INKY, MAP_BLINKY, MAP_CLYDE, MAP_PINKY]
ACTION_UP = 'U'
ACTION_DOWN = 'D'
ACTION_LEFT = 'L'
ACTION_RIGHT = 'R'
ACTIONS = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT]
ACTION_MOVE = {ACTION_UP: (-1, 0),
               ACTION_DOWN: (1, 0),
               ACTION_LEFT: (0, -1),
               ACTION_RIGHT: (0, 1)
               }
REWARD_GUM = 1
REWARD_DEFAULT = -1



class Ghost:
    def __init__(self, position, radar, direction_shift, file_sprite, pakman_position):
        self.__position = position
        self.__radar = radar
        self.__direction = None
        self.__direction_shift = direction_shift
        self.__file_sprite = file_sprite

        def follow_direction():
            pos_X, pos_Y = self.__position
            if self.__direction == "N":
                self.__position = (pos_X - 1, pos_Y)
            elif self.__direction == "S":
                self.__position = (pos_X + 1, pos_Y)
            elif self.__direction == "E":
                self.__position = (pos_X, pos_Y + 1)
            elif self.__direction == "O":
                self.__position = (pos_X, pos_Y - 1)

        def move(pacman_pos):
            pacman_X, pacman_Y = self.__radar.pakman_position
            ghost_X, ghost_Y = self.__position
            if self.__radar.radar[self.__direction] != MAP_WALL:
                follow_direction()
                return
            if pacman_X < self.__position and self.__radar.radar["N"] != MAP_WALL:
                if random() < direction_shift:
                    pass
            self.__radar.update_radar()

        def get_sprite():
            pass


class Environment:
    def __init__(self, str_map):
        self.__states = {
            "ghost_radar": {"NO": 0, "NE": 0, "SO": 0, "SE": 0,
                            "distance": 999999999999},
            "gum_radar": {"N": 0, "S": 0, "E": 0, "O": 0},
            "wall_radar": {"N": 0, "S": 0, "E": 0, "O": 0},
        }

        row = 0
        col = 0
        self.__init_position = None
        str_map = str_map.strip()
        self.__gums = []
        self.__ghosts = []
        self.__walls = []
        self.__gum_radar = None
        self.__wall_radar = None
        self.__pacman = None

        for line in str_map.strip().split('\n'):
            for item in line:
                self.__states[row, col] = item
                if item == MAP_GUM:
                    self.__gums.append((row, col))
                elif item == MAP_WALL:
                    self.__walls.append((row, col))
                elif item in MAP_GHOSTS:
                    self.__ghosts.append((row, col))
                elif item in MAP_PACMAN:
                    self.__pacman = (row, col)
                    self.__init_position = (row, col)

                col += 1
            row += 1
            col = 0

        if self.__pacman is None or self.__init_position is None:
            raise ValueError("Pacman not found in the game")

        self.__rows = row
        self.__cols = len(line)
        self.__reward_goal = REWARD_GUM
        self.__reward_ghost = -len(self.__states)
        self.__reward_wall = -2 * len(self.__states)
        self.__ghost_radar = GhostRadar().get(self.__ghosts, self.__pacman)
        self.__gum_radar = ShortRangeRadar.get(self.__pacman, self.__gums)
        self.__wall_radar = ShortRangeRadar.get(self.__pacman, self.__walls)

    def update_state(self, action):
        new_grid = self.__str_map

    def do(self, state, action):
        move = ACTION_MOVE[action]
        new_state = (state[0] + move[0], state[1] + move[1])

        if new_state in self.__gums:
            reward = self.__reward_goal
            state = new_state
        elif self.__states[new_state] in MAP_GHOSTS:
            reward = self.__reward_ghost
            state = self.__init_position
        elif self.__states[new_state] == MAP_WALL:
            reward = self.__reward_wall
        else:
            state = new_state
            reward = REWARD_DEFAULT

        return state, reward

        @property
        def states(self):
            return list(self.__states.keys())

        @property
        def start(self):
            return self.__start

        @property
        def goal(self):
            return self.__goal

        @property
        def height(self):
            return self.__rows

        @property
        def width(self):
            return self.__cols

        @property
        def is_wall(self, state):
            return self.__states[state] == MAP_WALL

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
