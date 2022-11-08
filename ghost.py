from actions import Action
from pacman import Pacman
from position import Position
from world import World


class Ghost:
  @property
  def position(self) -> Position:
    return self._position

  @property
  def isScared(self) -> bool:
    return self._isScared

  def __init__(self, position: Position, corner: Position, steps = 0, scaredSteps = 0, isScared=False, isScattering=False, stepsToSwitchMode=200, maxScaredSteps=100) -> None:
    self._position = position
    self._corner = corner
    self._steps = steps
    self._scaredSteps = scaredSteps
    self._isScared = isScared
    self._isScattering = isScattering
    self._stepsToSwitchMode = stepsToSwitchMode
    self._maxScaredSteps = maxScaredSteps

  # specific ghost subclasss must oerride this method to add movement logic !
  def move(self, world: World, pacman: Pacman) -> None:
    # call this logic before calling overridden behaviour in subclasses !
    if self.__isScared and self.__scaredSteps == self.__maxScaredSteps:
      self.__isScared = False
      self.__scaredSteps = 0

    if self.__steps == self.__stepsToSwitchMode:
      self.__isScattering = not self.__isScattering
      self.__steps = 0

    self.__steps += 1
    if self.__isScared:
      self.__scaredSteps += 1
