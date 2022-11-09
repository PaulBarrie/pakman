from actions import Action, Direction
from position import Position


# should be derived into KeyboardPakman, QTablePakman and NeuronsPakman
class Pacman:
  @property
  def position(self) -> Position:
    return self._position

  @property
  def lives(self) -> int:
    return self._lives

  @property
  def direction(self) -> Direction:
    return self._direction

  def __init__(self, position: Position, direction = Direction.WEST, lives: int = 3) -> None:
    self._position = position
    self._direction = direction
    self._lives = lives

  def die(self, respawnPosition: Position) -> None:
    if self._lives > 0:
      self._lives -= 1
    self._position = respawnPosition
    self._direction = Direction.WEST

  def _best_action(self) -> Action:
    raise NotImplemented()

  def step(self, game) -> tuple[Action, float]:
    raise NotImplemented()