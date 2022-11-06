# allow type hint for methods 
# returning a new instance of their own class
from __future__ import annotations
from enum import Enum
from core_game.actions import Action
from core_game.directions import Direction


class Position:
    @property
    def row(self) -> int:
        return self.__row

    @property
    def column(self) -> int:
        return self.__column

    def __init__(self, row: int, column: int) -> None:
        self.__row = row
        self.__column = column

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Position) \
               and self.__row == __o.row \
               and self.__column == __o.column

    def __hash__(self):
        return hash((self.__row, self.__column))

    def get_distance(self, other: Position) -> int:
        return abs(self.__row - other.row) + abs(self.__column - other.column)

    def apply_action(self, action: Action) -> Position:
        return Position(self.__row + action[0], self.__column + action[1])

    @staticmethod
    def position_apply_action(position: tuple[int, int], action: Action) -> Position:
        position = Position(position[0], position[1])
        return position.apply_action(action)

    def follow_direction(self, direction: Direction) -> Position:
        return self.apply_action(Action.from_direction(direction))

    @staticmethod
    def get_action_from(x: Position, to: Position) -> Action:
        relative_pos = RelativePosition.get(x, to)
        if relative_pos == RelativePosition.NE:
            if abs(x.column - to.column) < abs(x.row - to.row):
                return Action.UP
            else:
                return Action.RIGHT
        if relative_pos == RelativePosition.NW:
            if abs(x.column - to.column) < abs(x.row - to.row):
                return Action.UP
            else:
                return Action.LEFT
        if relative_pos == RelativePosition.SW:
            if abs(x.column - to.column) < abs(x.row - to.row):
                return Action.DOWN
            else:
                return Action.LEFT
        if relative_pos == RelativePosition.SE:
            if abs(x.column - to.column) < abs(x.row - to.row):
                return Action.DOWN
            else:
                return Action.RIGHT


class RelativePosition(int, Enum):

    NW = 1
    NE = 2
    SW = 3
    SE = 4

    """
        Gives the position of y wrt to x
    """

    @staticmethod
    def get(x: Position, y: Position):
        if x.column > y.column and y.row < x.row:
            return RelativePosition.NW
        if x.column < y.column and y.row < x.row:
            return RelativePosition.NE
        if x.column > y.column and y.row > x.row:
            return RelativePosition.SW
        if x.column < y.column and y.row > x.row:
            return RelativePosition.SE

    def is_in_direction(self, action: Action) -> bool:
        if action == Action.UP and (
                self == RelativePosition.NW or self == RelativePosition.NE):
            return True
        if action == Action.DOWN and (
                self == RelativePosition.SW or self == RelativePosition.SE):
            return True
        if action == Action.LEFT and (self == RelativePosition.NW or self == RelativePosition.SW):
            return True
        if action == Action.RIGHT and (self == RelativePosition.NE or self == RelativePosition.SE):
            return True

        return False

    @staticmethod
    def list() -> list[RelativePosition]:
        return [RelativePosition.NW, RelativePosition.NE, RelativePosition.SE, RelativePosition.SW]
