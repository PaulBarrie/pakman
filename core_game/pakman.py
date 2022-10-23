from copy import deepcopy

from core_game.actions import Action
from core_game.position import Position
from core_game.directions import Direction

# should be derived into KeyboardPakman, QTablePakman and NeuronsPakman
class Pakman:
    @property
    def position(self) -> Position:
        return self._position

    @property
    def lives(self) -> int:
        return self.__lives

    @property
    def direction(self) -> Direction:
        return self._direction

    @property
    def qtable(self):
        return None

    @property
    def history(self) -> list[float]:
        return []

    # @property
    # def current_state(self):
    #     return self.__current_state
    
    # @property
    # def last_action(self) -> Action:
    #     return self.__last_action
    
    # @property
    # def last_qvalue(self) -> float:
    #     return self.__last_qvalue

    def __init__(self, initial_position: Position, initial_direction=Direction.WEST, lives: int = 3) -> None:
        self._position = initial_position
        self._direction = initial_direction
        self.__lives = lives
        self.__current_state = None
        self.__last_action = None
        self.__last_qvalue = None

    def die(self) -> None:
        if self.__lives > 0:
            self.__lives -= 1
        self._direction = Direction.WEST

    def _best_action(self) -> Action:
        raise NotImplemented()

    def step(self) -> tuple[Action, float]:
        raise NotImplemented()

    def reset_pakman(self, position: Position) -> None:
        self._position = deepcopy(position)
        self.__lives = 3

    def reset(self, initial_position: Position, initial_state, environment, qtable, history):
        pass
