from actions import Action, Direction
from pacman import Pacman
from position import Position
from world import World

MOVE_COUNTDOWN = 200

class Ghost:
  @property
  def position(self) -> Position:
    return self._position

  @property
  def isScared(self) -> bool:
    return self._isScared

  def __init__(self, position: Position, corner: Position, steps = 0, scaredSteps = 0, isScared=False, isScattering=False, stepsToSwitchMode=40, maxScaredSteps=20) -> None:
    self._position = position
    self._corner = corner
    self._steps = steps
    self._scaredSteps = scaredSteps
    self._isScared = isScared
    self._isScattering = isScattering
    self._stepsToSwitchMode = stepsToSwitchMode
    self._maxScaredSteps = maxScaredSteps
    self._direction = Direction.WEST
    self.__moveCountDown = MOVE_COUNTDOWN

  # specific ghost subclasss must override this method to add movement logic !
  def move(self, world: World, pacman: Pacman) -> None:
    # call this logic before calling overridden behaviour in subclasses !
    if self.__moveCountDown:
      self.__moveCountDown -= 1
      return

    if self._isScared and self._scaredSteps == self._maxScaredSteps:
      self._isScared = False
      self._scaredSteps = 0

    if self._steps == self._stepsToSwitchMode:
      self._isScattering = not self._isScattering
      self._steps = 0

    self._steps += 1
    if self._isScared:
      self._scaredSteps += 1

    self.__moveCountDown = MOVE_COUNTDOWN 

  def _filterMoves(self, moves: list[Action]) -> list[Action]:
    return list(filter(
      lambda action: action.to_direction() != self._direction.getReverse(),
      moves
    ))
