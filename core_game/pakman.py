from core_agent import CoreAgent
from position import Position
from directions import Direction


# should be derived into KeyboardPakman, QTablePakman and NeuronsPakman
class Pakman(CoreAgent):
    @property
    def lives(self) -> int:
        return self.__lives

    def __init__(self, initial_position: Position, lives: int = 3):
        super().__init__(initial_position)
        self.__initial_position = initial_position
        self.__lives = lives


    def die(self) -> None:
        if self.__lives > 0:
            self.__lives -= 1
        self._position = self.__initial_position