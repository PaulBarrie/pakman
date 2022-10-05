from __future__ import annotations
from enum import Enum

class Distance(str, Enum):
    ONE = "1"
    TWO = "2"
    THREE_OR_MORE = "SE3"

    @staticmethod
    def list() -> list[Distance]:
        return [Distance.ONE, Distance.TWO, Distance.THREE_OR_MORE]

    @staticmethod
    def int_to_distance(numeric_distance: int) -> Distance:
        if numeric_distance == 1:
            return Distance.ONE
        if numeric_distance == 2:
            return Distance.TWO
        return Distance.THREE_OR_MORE


# class GhostDirections:
#     N = "N"
#     S = "S"
#     E = "E"
#     O = "O"
#     NO = "NO"
#     NE = "NE"
#     SO = "SO"
#     SE = "SE"

#     @staticmethod
#     def list():
#         return [GhostDirections.NO, GhostDirections.NE, GhostDirections.SE, GhostDirections.SO]


# class ActionMoves:
#     N = "N"
#     S = "S"
#     O = "O"
#     E = "E"

#     @staticmethod
#     def list():
#         return [ActionMoves.N, ActionMoves.S, ActionMoves.O, ActionMoves.E]
