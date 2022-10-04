from core_game.core_agent import CoreAgent
from core_game.position import Position
from core_game.directions import Direction


# should be derived into KeyboardPakman, QTablePakman and NeuronsPakman
class Pakman(CoreAgent):
    @property
    def lives(self) -> int:
        return self.__lives

    @property
    def direction(self) -> Direction:
        return self.__direction

    def __init__(self, initial_position: Position, initial_direction = Direction.WEST, lives: int = 3):
        super().__init__(initial_position)
        self.__initial_position = initial_position
        self.__direction = initial_direction
        self.__lives = lives


    def die(self) -> None:
        if self.__lives > 0:
            self.__lives -= 1
        self._position = self.__initial_position
        self.__direction = Direction.WEST