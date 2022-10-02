import numpy as np
from environment.metrics import *

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

        for gumX, gumY in targets:
            if gumX == pos_X - 1 and gumY == pos_Y:
                radar[ActionMoves.N] = 1
            elif gumX == pos_X + 1 and gumY == pos_Y:
                radar[ActionMoves.S] = 1
            elif gumX == pos_X and gumY == pos_Y + 1:
                radar[ActionMoves.E] = 1
            elif gumX == pos_X and gumY == pos_Y - 1:
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
        direction = ""
        if closest_X < pacman_X and pacman_Y < closest_Y:
            direction = GhostDirections.NE
        elif pacman_X < closest_X and pacman_Y < closest_Y:
            direction = GhostDirections.NO
        elif closest_X < pacman_X and pacman_Y < closest_Y:
            direction = GhostDirections.SO
        elif pacman_X < closest_X and pacman_Y < closest_Y:
            direction = GhostDirections.SE

        return {
            "direction": direction,
            "distance": distance
        }
