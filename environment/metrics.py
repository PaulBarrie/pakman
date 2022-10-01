class Distances:
    DIST_1 = "1"
    DIST_2 = "2"
    DIST_3 = "SE3"

    @staticmethod
    def list():
        return [Distances.DIST_1, Distances.DIST_2, Distances.DIST_3]


class GhostDirections:
    N = "N"
    S = "S"
    E = "E"
    O = "O"
    NO = "NO"
    NE = "NE"
    SO = "SO"
    SE = "SE"

    @staticmethod
    def list():
        return [GhostDirections.NO, GhostDirections.NE, GhostDirections.SE, GhostDirections.SO]


class ActionMoves:
    N = "N"
    S = "S"
    O = "O"
    E = "E"

    @staticmethod
    def list():
        return [ActionMoves.N, ActionMoves.S, ActionMoves.O, ActionMoves.E]
