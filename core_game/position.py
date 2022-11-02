# allow type hint for methods 
# returning a new instance of their own class
from __future__ import annotations
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

    # Dirty method with if/else nested to simplify
    @staticmethod
    def get_direction_from(x: Position, y: Position) -> Direction:
        relative_pos = RelativePosition.get(x, y)
        if relative_pos == RelativePosition.NE:
            if abs(x.column - y.column) < abs(x.row - y.row):
                return Direction.NORTH
            else:
                return Direction.EAST
        if relative_pos == RelativePosition.NW:
            if abs(x.column - y.column) < abs(x.row - y.row):
                return Direction.NORTH
            else:
                return Direction.WEST
        if relative_pos == RelativePosition.SW:
            if abs(x.column - y.column) < abs(x.row - y.row):
                return Direction.SOUTH
            else:
                return Direction.WEST
        if relative_pos == RelativePosition.SE:
            if abs(x.column - y.column) < abs(x.row - y.row):
                return Direction.SOUTH
            else:
                return Direction.EAST

    def get_distance(self, other: Position) -> int:
        return abs(self.__row - other.row) + abs(self.__column - other.column)

    def apply_action(self, action: Action) -> Position:
        return Position(self.__row + action[0], self.__column + action[1])

    def follow_direction(self, direction: Direction) -> Position:
        return self.apply_action(Action.from_direction(direction))


class RelativePosition:
    NW = "1"
    NE = "2"
    SW = "3"
    SE = "4"

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

    def is_in_direction(self, direction: Direction) -> bool:
        if direction == Direction.NORTH and (
                self == RelativePosition.NW or self == RelativePosition.NE):
            return True
        if direction == Direction.SOUTH and (
                self == RelativePosition.SW or self == RelativePosition.SE):
            return True
        if direction == Direction.WEST and (self == RelativePosition.NW or self == RelativePosition.SW):
            return True
        if direction == Direction.EAST and (self == RelativePosition.NE or self == RelativePosition.SE):
            return True

        return False

    @staticmethod
    def list() -> list[RelativePosition]:
        return [RelativePosition.NW, RelativePosition.NE, RelativePosition.SE, RelativePosition.SW]