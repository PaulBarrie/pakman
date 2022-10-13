from __future__ import annotations
from enum import Enum

class Direction(str, Enum):
    NORTH = "North"
    SOUTH = "South"
    WEST = "West"
    EAST = "East"

    def is_reverse(self, other_direction: Direction) -> bool:
        return (self == Direction.NORTH and other_direction == Direction.SOUTH) \
            or (self == Direction.SOUTH and other_direction == Direction.NORTH) \
            or (self == Direction.WEST and other_direction == Direction.EAST) \
            or (self == Direction.EAST and other_direction == Direction.WEST)

    @staticmethod
    def as_list() -> list[Direction]:
        return [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST]
