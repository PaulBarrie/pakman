from blinky import Blinky
from ghost import Ghost
from pacman import Pacman
from position import Position
from utils import manhattan_distance
from world import World


class Inky(Ghost):
  def __init__(self, position: Position, corner: Position, blinky: Blinky) -> None:
    super().__init__(position=position, corner=corner)
    self.__blinky = blinky

  def move(self, world: World, pacman: Pacman) -> None:
    super().move(world, pacman)

    target = self.__calculateTarget(pacman)
    if self.__isScattering or self.__isScared:
      target = self.__corner

    legal_actions = world.get_legal_actions(self.__position)
    best_action = list(sorted(
      legal_actions,
      key=lambda action: manhattan_distance(self.__position.apply_action(action), target)
    ))[0]

    self.__position = self.__position.apply_action(best_action)

  # target is the result of a 180° rotation of blinky's position 
  # around the tile in front of Pacman
  def __calculateTarget(self, pacman: Pacman) -> Position:
    rotationOrigin = pacman.position.follow_direction(pacman.direction)
    targetRow = 2 * rotationOrigin.row - self.__blinky.position.row
    targetColumn = 2 * rotationOrigin.column - self.__blinky.position.column
    return Position(targetRow, targetColumn)