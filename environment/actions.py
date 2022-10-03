from __future__ import annotations
from enum import Enum
from this import d
from metrics import ActionMoves

class Action(tuple[int, int], Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def to_direction(self) -> str:
        if self == Action.UP:
            return ActionMoves.N
        if self == Action.DOWN:
            return ActionMoves.S
        if self == Action.LEFT:
            return ActionMoves.O
        return ActionMoves.E

    @staticmethod
    def from_direction(direction: str) -> Action:
        if direction == ActionMoves.N:
            return Action.UP
        if direction == ActionMoves.S:
            return Action.DOWN
        if direction == ActionMoves.O:
            return Action.LEFT
        if direction == ActionMoves.E:
            return Action.RIGHT
        
        raise ValueError("Invalid direction")


    @staticmethod
    def as_list() -> list[tuple[int, int]]:
        return [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]