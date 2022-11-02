from __future__ import annotations
from enum import Enum
from core_game.directions import Direction


class Action(tuple[int, int], Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def to_direction(self) -> Direction:
        if self == Action.UP:
            return Direction.NORTH
        if self == Action.DOWN:
            return Direction.SOUTH
        if self == Action.LEFT:
            return Direction.WEST
        return Direction.EAST

    @staticmethod
    def from_direction(direction: Direction) -> Action:
        if direction == Direction.NORTH:
            return Action.UP
        if direction == Direction.SOUTH:
            return Action.DOWN
        if direction == Direction.WEST:
            return Action.LEFT
        if direction == Direction.EAST:
            return Action.RIGHT

        raise ValueError("Invalid direction")

    @staticmethod
    def as_list() -> list[Action]:
        return [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]
