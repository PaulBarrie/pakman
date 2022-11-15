from actions import Action, Direction
from pacman import Pacman
from position import Position
from world import World

# MOVE_COUNTDOWN = 200

class Ghost:
  @property
  def position(self) -> Position:
    return self._position

  @property
  def isScared(self) -> bool:
    return self._isScared

  def __init__(self, position: Position, corner: Position, steps=0, isScared=False, isScattering=False, maxChaseSteps=20, maxScatterSteps=30, maxScaredSteps=20) -> None:
    self._position = position
    self.__initialPosition = position
    self._corner = corner
    self._steps = steps
    self._isScared = isScared
    self._isScattering = isScattering
    self._maxChaseSteps = maxChaseSteps
    self._maxScatterSteps = maxScatterSteps
    self._maxScaredSteps = maxScaredSteps
    self._direction = Direction.WEST
    # self.__moveCountDown = MOVE_COUNTDOWN

  # specific ghost subclasss must override this method to add movement logic !
  def move(self, world: World, pacman: Pacman) -> None:
    # call this logic before calling overridden behaviour in subclasses !

    if self._isScared and self._steps == self._maxScaredSteps:
      self._isScared = False
      self._steps = 0

    elif self._isScattering and self._steps == self._maxScatterSteps:
      self._isScattering = False
      self._steps = 0

    elif not self._isScattering and self._steps == self._maxChaseSteps:
      self._isScattering = True
      self._steps = 0

    else: 
      self._steps += 1

  def reset(self) -> None:
    self._position = self.__initialPosition
    self._direction = Direction.WEST

  def _filterMoves(self, moves: list[Action]) -> list[Action]:
    return list(filter(
      lambda action: action.to_direction() != self._direction.getReverse(),
      moves
    ))
