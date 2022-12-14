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

    def __init__(self, initial_position: Position, initial_direction = Direction.WEST, lives: int = 3) -> None:
        self._position = initial_position
        self._direction = initial_direction
        self.__lives = lives

    def move_to(self, position: Position) -> None:
        self._position = position

    def die(self) -> None:
        # print("The Punjabi Warrior has died !")
        if self.__lives > 0:
            self.__lives -= 1
        self._direction = Direction.WEST
    
    def heat(self) -> None:
      pass

    def refreshState(
      self,
      ghost_positions: list[Position],
      gum_positions: list[Position], 
      wall_positions: list[Position]
    ) -> None:
      pass

    def _best_action(self) -> Action:
        raise NotImplemented()

    def step(self) -> tuple[Action, float]:
        raise NotImplemented()