import numpy as np
from core_game.position import Position
from core_game.actions import Action
from environment.metrics import *


class State:
    STATE_VAL_SEPARATOR = ""

    def __init__(self):
        self.__ghost_radar = None
        self.__gum_radar = None
        self.__wall_radar = None

    def update(self, ghosts: list[(int,int)], pacman: tuple[int, int], gums: list[(int, int)], walls: list[(int, int)]):
        self.__ghost_radar = GhostRadar().get(ghosts, pacman)
        self.__gum_radar = ShortRangeRadar.get(pacman, gums)
        self.__wall_radar = ShortRangeRadar.get(pacman, walls)

    def __hash__(self) -> int:
        return hash(( 
            hash(self.__gum_radar), 
            hash(self.__wall_radar), 
            hash(self.__ghost_radar) 
        ))

    def __repr__(self) -> str:
        ghost_state = self.__state_str(self.__ghost_radar)
        gum_state = self.__state_str(self.__gum_radar)
        wall_state = self.__state_str(self.__wall_radar)

        return f'ghost: {ghost_state}, gums: {gum_state}, walls: {wall_state}'

    def __state_str(self, state: dict) -> str:
        return State.STATE_VAL_SEPARATOR.join([key for key, val in state.items() if val == 1])


class ShortRangeRadar:
    @property
    def north(self) -> bool:
        return self.__north

    @property
    def south(self) -> bool:
        return self.__south

    @property
    def west(self) -> bool:
        return self.__west

    @property
    def east(self) -> bool:
        return self.__east

    def __init__(self, north: bool, south: bool, west: bool, east: bool) -> None:
        self.__north = north
        self.__south = south
        self.__west = west
        self.__east = east

    def update(self, position: Position, targets: list[Position]) -> None:
        north_position = position.apply_action(Action.UP)
        south_position = position.apply_action(Action.DOWN)
        west_position = position.apply_action(Action.LEFT)
        east_position = position.apply_action(Action.RIGHT)

        self.__north = north_position in targets
        self.__south = south_position in targets
        self.__west = west_position in targets
        self.__east = east_position in targets


    def __hash__(self) -> int:
        return hash((self.__north, self.__south, self.__west, self.__east))

    # @staticmethod
    # def get(position, targets) -> dict:
    #     pos_X, pos_Y = position
    #     radar = {
    #         ActionMoves.N: 0,
    #         ActionMoves.S: 0,
    #         ActionMoves.E: 0,
    #         ActionMoves.O: 0
    #     }

    #     for targetX, targetY in targets:
    #         if targetX == pos_X - 1 and targetY == pos_Y:
    #             radar[ActionMoves.N] = 1
    #         elif targetX == pos_X + 1 and targetY == pos_Y:
    #             radar[ActionMoves.S] = 1
    #         elif targetX == pos_X and targetY == pos_Y + 1:
    #             radar[ActionMoves.E] = 1
    #         elif targetX == pos_X and targetY == pos_Y - 1:
    #             radar[ActionMoves.O] = 1
    #     return radar


class GhostRadar:
    """
        Directions
            NE  | NO
                |
        ----------------
            SE  | SO
                |
    """
    @property
    def north(self) -> bool:
        return self.__north
    
    @property
    def south(self) -> bool:
        return self.__south

    @property
    def west(self) -> bool:
        return self.__west

    @property
    def east(self) -> bool:
        return self.__east

    @property
    def distance(self) -> Distance:
        return self.__distance

    def __init__(self, north, south, west, east, distance: Distance) -> None:
        self.__north = north
        self.__south = south
        self.__west = west
        self.__east = east
        self.__distance = distance

    def __hash__(self) -> int:
        return hash(self.__north, self.__south, self.__west, self.__east, self.__distance)

    def update(self, pakman_position: Position, ghost_positions: list[Position]) -> None:
        closest_ghost_position = list(sorted(
            ghost_positions,
            key = lambda gp: gp.get_distance(pakman_position)
        ))[0]

        self.__north = closest_ghost_position.row < pakman_position.row
        self.__south = closest_ghost_position.row > pakman_position.row
        self.__west = closest_ghost_position.column < pakman_position.column
        self.__east = closest_ghost_position.column > pakman_position.column

        dist = closest_ghost_position.get_distance(pakman_position)
        if dist == 1:
            self.__distance = Distance.ONE
            return
        if dist == 2:
            self.__distance = Distance.TWO
            return
        self.__distance = Distance.THREE_OR_MORE


    # @staticmethod
    # def get(ghost_positions, pacman) -> dict:
    #     pacman_X, pacman_Y = pacman
    #     ghost_dist = [abs(pacman_X - x) + abs(pacman_Y - y) for x, y in ghost_positions]
    #     distance = min(ghost_dist)
    #     closest_X, closest_Y = ghost_positions[np.argmin(ghost_dist)]
    #     direction = {
    #         ActionMoves.N: 0,
    #         ActionMoves.S: 0,
    #         ActionMoves.E: 0,
    #         ActionMoves.O: 0,
    #     }

    #     if closest_X < pacman_X:
    #         direction[ActionMoves.N] = 1
    #     else:
    #         direction[ActionMoves.S] = 1
    #     if closest_Y < pacman_Y:
    #         direction[ActionMoves.O] = 1
    #     else:
    #         direction[ActionMoves.E] = 1

    #     return {
    #         "direction": direction,
    #         "distance": distance
    #     }