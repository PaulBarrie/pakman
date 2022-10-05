from __future__ import annotations
from core_game.actions import Action
from core_game.position import Position
from environment.metrics import *
from environment.state import State

MAP_WALL = '#'
MAP_GUM = '.'
MAP_PACMAN = 'P'
MAP_EMPTY = ' '
MAP_INKY = 'I'
MAP_BLINKY = 'B'
MAP_CLYDE = 'C'
MAP_PINKY = 'R'
MAP_GHOSTS = [MAP_INKY, MAP_BLINKY, MAP_CLYDE, MAP_PINKY]

# ACTION_MOVE = {
#     ActionMoves.N: (-1, 0),
#     ActionMoves.S: (1, 0),
#     ActionMoves.O: (0, -1),
#     ActionMoves.E: (0, 1)
# }
REWARD_GUM = 1
REWARD_DEFAULT = -1
NB_STATES = 2 ** 4 * 2 ** 4 * 8 * 4
REWARD_GHOST = -NB_STATES
REWARD_WALL = -2 * REWARD_GHOST


# class Ghost:
#     def __init__(self, position, radar, direction_shift, file_sprite, walls):
#         self.__position = position
#         self.__radar = radar
#         self.__direction = None
#         self.__direction_shift = direction_shift
#         self.__file_sprite = file_sprite
#         self.__walls = walls

#     def follow_direction(self):
#         pos_X, pos_Y = self.__position
#         if self.__direction == ActionMoves.N:
#             position = (pos_X - 1, pos_Y)
#         elif self.__direction == ActionMoves.S:
#             position = (pos_X + 1, pos_Y)
#         elif self.__direction == ActionMoves.E:
#             position = (pos_X, pos_Y + 1)
#         elif self.__direction == ActionMoves.O:
#             position = (pos_X, pos_Y - 1)
#         if position in self.__walls:
#             raise Exception("Ghost can't move to wall")
#         self.__position = position

#         """
#             If direction, follow it
#             If cant check two best directions, take the 1st one and change direction
#         """

#     def move(self, pacman_pos):
#         pacman_X, pacman_Y = self.__radar.pakman_position
#         ghost_X, ghost_Y = self.__position

#         best_directions = []

#         if pacman_X < ghost_X:
#             best_directions.append(ActionMoves.N)
#         else:
#             best_directions.append(ActionMoves.S)

#         if pacman_Y < ghost_Y:
#             best_directions.append(ActionMoves.O)
#         else:
#             best_directions.append(ActionMoves.E)

#         if self.__direction in best_directions:
#             try:
#                 self.follow_direction()
#             except:
#                 pass
#         else:
#             for direction in best_directions:
#                 try:
#                     self.follow_direction()
#                     break
#                 except:
#                     continue

#         def get_sprite():
#             pass


class Environment:
    # @property
    # def state(self):
    #     return self.__state

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

    def __init__(self, width: int, height: int, gums: list[Position], walls: list[Position], pakman_position: Position, ghost_positions: dict[str, Position]) -> None:
        self.__width = width
        self.__height = height
        self.__gums = gums
        self.__walls = walls
        self.__initial_pakman_position = pakman_position
        self.__pakman_position = pakman_position
        self.__ghost_positions = ghost_positions

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

    # def __init__(self, str_map):
    #     row = 0
    #     col = 0
    #     self.__init_position = None
    #     str_map = str_map.strip()
    #     self.__gums = []
    #     self.__ghosts = []
    #     self.__walls = []
    #     self.__pacman = None
    #     self.__state = None

    #     for line in str_map.strip().split('\n'):
    #         for item in line:
    #             if item == MAP_GUM:
    #                 self.__gums.append((row, col))
    #             elif item == MAP_WALL:
    #                 self.__walls.append((row, col))
    #             elif item in MAP_GHOSTS:
    #                 self.__ghosts.append((row, col))
    #             elif item == MAP_PACMAN:
    #                 self.__pacman = (row, col)
    #                 self.__init_position = (row, col)

    #             col += 1
    #         row += 1
    #         col = 0

    #     if self.__pacman is None or self.__init_position is None:
    #         raise ValueError("Pacman not found in the game")

    #     self.__init_ghosts = self.__ghosts.copy()
    #     self.__init_pacman = self.__pacman

    #     self.__state = State()
    #     self.__state.update(self.__ghosts, self.__pacman, self.__gums, self.__walls)

    #     self.__rows = row
    #     self.__cols = len(line)
    #     self.__reward_goal = REWARD_GUM
    #     self.__reward_ghost = REWARD_GHOST
    #     self.__reward_wall = REWARD_WALL
    #     self.reward_end = len(self.__gums)

    # def update(self, position):
    #     self.__pacman = position
    #     self.__state.update(self.__ghosts, position, self.__gums, self.__walls)

    def do(self, action: Action, state=None) -> tuple[Position, State, float, bool]:
        # move = ACTION_MOVE[action]
        # pos_X, pos_Y = self.__pacman
        # new_position = (pos_X + move[0], pos_Y + move[1])

        # if new_position in self.__ghosts:
        #     reward = self.__reward_ghost
        #     self.__ghosts = self.__init_ghosts.copy()
        #     self.__pacman = self.__init_pacman.copy()
        #     new_position = self.__init_position
        # elif new_position in self.__walls:
        #     reward = self.__reward_wall
        #     new_position = self.__pacman
        # elif new_position in self.__gums:
        #     reward = self.__reward_goal
        #     self.__gums.remove(new_position)
        # else:
        #     reward = REWARD_DEFAULT

        # self.update(new_position)
        # return reward, repr(self.__state)
        next_position = self.__pakman_position.apply_action(action)
        next_state = self._calculate_state(next_position)

        if next_position in self.__ghosts:
            self.__pakman_position = self.__initial_pakman_position
            return (self.__initial_pakman_position, self._calculate_state(self.__initial_pakman_position), REWARD_GHOST, True)

        if next_position in self.__walls:
            return (self.__pakman_position, state, REWARD_WALL, False)

        if next_position in self.__gums:
            self.__pakman_position = next_position
            self.__gums.remove(next_position)
            return (next_position, next_state, REWARD_GUM, False)

        self.__pakman_position = next_position
        return (next_position, next_state, REWARD_DEFAULT)
        

    def _calculate_state(self, position: Position) -> State:
        raise NotImplemented()
            
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
