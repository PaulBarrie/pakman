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

    def get_distance(self, other: Position) -> int:
        return abs(self.__row - other.row) + abs(self.__column - other.column)

    def apply_action(self, action: Action) -> Position:
        return Position(self.__row + action[0], self.__column + action[1])

    def follow_direction(self, direction: Direction) -> Position:
        return self.apply_action(Action.from_direction(direction))
