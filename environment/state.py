import numpy as np
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

    def __repr__(self) -> str:
        ghost_state = self.__state_str(self.__ghost_radar)
        gum_state = self.__state_str(self.__gum_radar)
        wall_state = self.__state_str(self.__wall_radar)

        return f'ghost: {ghost_state}, gums: {gum_state}, walls: {wall_state}'

    def __state_str(self, state: dict) -> str:
        return State.STATE_VAL_SEPARATOR.join([key for key, val in state.items() if val == 1])


class ShortRangeRadar:
    @staticmethod
    def get(position, targets) -> dict:
        pos_X, pos_Y = position
        radar = {
            ActionMoves.N: 0,
            ActionMoves.S: 0,
            ActionMoves.E: 0,
            ActionMoves.O: 0
        }

        for targetX, targetY in targets:
            if targetX == pos_X - 1 and targetY == pos_Y:
                radar[ActionMoves.N] = 1
            elif targetX == pos_X + 1 and targetY == pos_Y:
                radar[ActionMoves.S] = 1
            elif targetX == pos_X and targetY == pos_Y + 1:
                radar[ActionMoves.E] = 1
            elif targetX == pos_X and targetY == pos_Y - 1:
                radar[ActionMoves.O] = 1
        return radar


class GhostRadar:
    """
        Directions
            NE  | NO
                |
        ----------------
            SE  | SO
                |
    """

    @staticmethod
    def get(ghost_positions, pacman) -> dict:
        pacman_X, pacman_Y = pacman
        ghost_dist = [abs(pacman_X - x) + abs(pacman_Y - y) for x, y in ghost_positions]
        distance = min(ghost_dist)
        closest_X, closest_Y = ghost_positions[np.argmin(ghost_dist)]
        direction = {
            ActionMoves.N: 0,
            ActionMoves.S: 0,
            ActionMoves.E: 0,
            ActionMoves.O: 0,
        }

        if closest_X < pacman_X:
            direction[ActionMoves.N] = 1
        else:
            direction[ActionMoves.S] = 1
        if closest_Y < pacman_Y:
            direction[ActionMoves.O] = 1
        else:
            direction[ActionMoves.E] = 1

        return {
            "direction": direction,
            "distance": distance
        }
