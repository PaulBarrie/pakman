import numpy as np


class ShortRangeRadar:
    @staticmethod
    def get(position, targets) -> dict:
        pos_X, pos_Y = position
        radar = {
            "N": 0,
            "S": 0,
            "E": 0,
            "O": 0
        }

        for gumX, gumY in targets:
            if gumX == pos_X - 1 and gumY == pos_Y:
                radar["N"] = 1
            elif gumX == pos_X + 1 and gumY == pos_Y:
                radar["S"] = 1
            elif gumX == pos_X and gumY == pos_Y + 1:
                radar["E"] = 1
            elif gumX == pos_X and gumY == pos_Y - 1:
                radar["O"] = 1
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
            direction = "NE"
        elif pacman_X < closest_X and pacman_Y < closest_Y:
            direction = "NO"
        elif closest_X < pacman_X and pacman_Y < closest_Y:
            direction = "SO"
        elif pacman_X < closest_X and pacman_Y < closest_Y:
            direction = "SE"

        return {
            "direction": direction,
            "distance": distance
        }
