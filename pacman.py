from actions import Action, Direction
from position import Position


# should be derived into KeyboardPakman, QTablePakman and NeuronsPakman
class Pacman:
  @property
  def position(self) -> Position:
    return self._position

  @property
  def lives(self) -> int:
    return self.__lives

  @property
  def direction(self) -> Direction:
    return self._direction

  def __init__(self, position: Position, direction = Direction.WEST, lives: int = 3) -> None:
    self._position = position
    self._direction = direction
    self.__lives = lives

  def die(self, respawnPosition: Position) -> None:
    if self.__lives > 0:
      self.__lives -= 1
    self._position = respawnPosition
    self._direction = Direction.WEST
    # print("Pacman died")

  def _best_action(self) -> Action:
    raise NotImplemented()

  def step(self, game) -> tuple[Action, float]:
    raise NotImplemented()