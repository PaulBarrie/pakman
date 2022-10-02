from random import random
from environment.metrics import *
from enum import Enum

from environment.radars import ShortRangeRadar, GhostRadar

MAP_WALL = '#'
MAP_GUM = '.'
MAP_PACMAN = 'P'
MAP_EMPTY = ' '
MAP_INKY = 'I'
MAP_BLINKY = 'B'
MAP_CLYDE = 'C'
MAP_PINKY = 'R'
MAP_GHOSTS = [MAP_INKY, MAP_BLINKY, MAP_CLYDE, MAP_PINKY]

ACTION_MOVE = {
    ActionMoves.N: (-1, 0),
    ActionMoves.S: (1, 0),
    ActionMoves.O: (0, -1),
    ActionMoves.E: (0, 1)
}
REWARD_GUM = 1
REWARD_DEFAULT = -1
NB_STATES = 2 ** 4 * 2 ** 4 * 8 * 4
REWARD_GHOST = -NB_STATES
REWARD_WALL = -2 * REWARD_GHOST


class Ghost:
    def __init__(self, position, radar, direction_shift, file_sprite, walls):
        self.__position = position
        self.__radar = radar
        self.__direction = None
        self.__direction_shift = direction_shift
        self.__file_sprite = file_sprite
        self.__walls = walls

        def follow_direction():
            pos_X, pos_Y = self.__position
            if self.__direction == ActionMoves.N:
                position = (pos_X - 1, pos_Y)
            elif self.__direction == ActionMoves.S:
                position = (pos_X + 1, pos_Y)
            elif self.__direction == ActionMoves.E:
                position = (pos_X, pos_Y + 1)
            elif self.__direction == ActionMoves.O:
                position = (pos_X, pos_Y - 1)
            if position in self.__walls:
                raise Exception("Ghost can't move to wall")
            self.__position = position

        """
            If direction, follow it
            If cant check two best directions, take the 1st one and change direction
        """

        def move(pacman_pos):
            pacman_X, pacman_Y = self.__radar.pakman_position
            ghost_X, ghost_Y = self.__position

            best_directions = []

            if pacman_X < ghost_X:
                best_directions.append(ActionMoves.N)
            else:
                best_directions.append(ActionMoves.S)

            if pacman_Y < ghost_Y:
                best_directions.append(ActionMoves.O)
            else:
                best_directions.append(ActionMoves.E)

            if self.__direction in best_directions:
                try:
                    follow_direction()
                except:
                    pass
            else:
                for direction in best_directions:
                    try:
                        follow_direction()
                        break
                    except:
                        continue

        def get_sprite():
            pass


class Environment:
    KEYS_STATE_CHARACTER_JOIN = '_'
    RADAR_STATE_CHARACTER_JOIN = '|'

    def __init__(self, str_map):
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
        self.__ghost_radar = None
        self.__gum_radar = None
        self.__wall_radar = None
        self.__state = None

        a = str_map
        b = str_map.split('\n')
        for line in str_map.split('\n'):
            for item in line:
                if item == MAP_GUM:
                    self.__gums.append((row, col))
                elif item == MAP_WALL:
                    self.__walls.append((row, col))
                elif item in MAP_GHOSTS:
                    self.__ghosts.append((row, col))
                elif item == MAP_PACMAN:
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
        self.__reward_ghost = REWARD_GHOST
        self.__reward_wall = REWARD_WALL
        self.update(self.__pacman)

    def update_radars(self):
        self.__ghost_radar = GhostRadar().get(self.__ghosts, self.__pacman)
        self.__gum_radar = ShortRangeRadar.get(self.__pacman, self.__gums)
        self.__wall_radar = ShortRangeRadar.get(self.__pacman, self.__walls)

    def get_state(self):
        return Environment.KEYS_STATE_CHARACTER_JOIN.join([self.__ghost_radar, self.__gum_radar, self.__wall_radar])

    def update_state(self):
        ghost_state = Environment.KEYS_STATE_CHARACTER_JOIN.join([k + str(v) for k, v in self.__ghost_radar.items()])
        gum_state = Environment.KEYS_STATE_CHARACTER_JOIN.join([k + str(v) for k, v in self.__gum_radar.items()])
        wall_state = Environment.KEYS_STATE_CHARACTER_JOIN.join([k + str(v) for k, v in self.__wall_radar.items()])

        self.__state = Environment.RADAR_STATE_CHARACTER_JOIN.join([ghost_state, gum_state, wall_state])

    def update(self, position):
        self.__pacman = position
        self.update_radars()
        self.update_state()

    def do(self, action):
        move = ACTION_MOVE[action]
        pos_X, pos_Y = self.__pacman
        new_position = (pos_X + move[0], pos_Y + move[1])

        if new_position in self.__gums:
            reward = self.__reward_goal
            self.__gums.remove(new_position)
            self.update(new_position)
        elif new_position in self.__ghosts:
            reward = self.__reward_ghost
            self.update(self.__init_position)
        elif new_position in self.__walls:
            reward = self.__reward_wall
        else:
            reward = REWARD_DEFAULT
            self.update(new_position)

        return self.__state, reward

    @property
    def state(self):
        return self.__state

    @property
    def start(self):
        return self.__init_position

    @property
    def height(self):
        return self.__rows

    @property
    def width(self):
        return self.__cols

    @property
    def is_wall(self, state):
        return self.__states[state] == MAP_WALL

    @property
    def walls(self):
        return self.__walls

    @property
    def ghosts(self):
        return self.__ghosts

    @property
    def gums(self):
        return self.__gums

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
