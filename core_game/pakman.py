from core_game.actions import Action
from core_game.position import Position
from core_game.directions import Direction


# should be derived into KeyboardPakman, QTablePakman and NeuronsPakman
class Pakman:
    @property
    def position(self) -> Position:
        return self.__position

    @property
    def lives(self) -> int:
        return self.__lives

    @property
    def direction(self) -> Direction:
        return self.__direction

    def __init__(self, initial_position: Position, initial_direction = Direction.WEST, lives: int = 3) -> None:
        self.__position = initial_position
        self.__direction = initial_direction
        self.__lives = lives

    def move(self, position: Position) -> None:
        self.__position = position

    def die(self) -> None:
        if self.__lives > 0:
            self.__lives -= 1
        self.__direction = Direction.WEST

    def _best_action(self) -> Action:
        raise NotImplemented()

    def step(self) -> tuple[Action, float]:
        raise NotImplemented()