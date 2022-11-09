# allow type hint for methods 
# returning a new instance of their own class
from __future__ import annotations
from actions import Action, Direction



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

    def __hash__(self) -> int:
        return hash((self.__row, self.__column))

    def __repr__(self) -> str:
        return f"row {self.__row} column {self.__column}"

    def get_distance(self, other: Position) -> int:
        return abs(self.__row - other.row) + abs(self.__column - other.column)

    def apply_action(self, action: Action) -> Position:
        return Position(self.__row + action[0], self.__column + action[1])

    def follow_direction(self, direction: Direction) -> Position:
        return self.apply_action(Action.from_direction(direction))
