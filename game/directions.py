from __future__ import annotations
from enum import Enum

class Direction(str, Enum):
    NORTH = "North"
    SOUTH = "South"
    WEST = "West"
    EAST = "East"

    @staticmethod
    def as_list() -> list[Direction]:
        return [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST]
