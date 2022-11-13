from blinky import Blinky
from ghost import Ghost
from pacman import Pacman
from position import Position
from utils import manhattan_distance
from world import World


class Inky(Ghost):
  def __init__(self, position: Position, corner: Position, blinky: Blinky) -> None:
    super().__init__(position=position, corner=corner)
    self._blinky = blinky

  def move(self, world: World, pacman: Pacman) -> None:
    super().move(world, pacman)

    target = self._calculateTarget(pacman)
    if self._isScattering or self._isScared:
      target = self._corner

    legal_actions = self._filterMoves(world.get_legal_actions(self._position))
    best_action = list(sorted(
      legal_actions,
      key=lambda action: manhattan_distance(self._position.apply_action(action), target)
    ))[0]

    self._position = self._position.apply_action(best_action)
    self._direction = best_action.to_direction()

  # target is the result of a 180° rotation of blinky's position 
  # around the tile in front of Pacman
  def _calculateTarget(self, pacman: Pacman) -> Position:
    rotationOrigin = pacman.position.follow_direction(pacman.direction)
    targetRow = 2 * rotationOrigin.row - self._blinky.position.row
    targetColumn = 2 * rotationOrigin.column - self._blinky.position.column
    return Position(targetRow, targetColumn)