from ghost import Ghost
from pacman import Pacman
from position import Position
from utils import manhattan_distance
from world import World


class Blinky(Ghost):
  def _init_(self, position: Position, corner: Position) -> None:
    super()._init_(position=position, corner=corner)

  def move(self, world: World, pacman: Pacman) -> None:
    super().move(world, pacman)

    target = pacman.position
    if self._isScattering or self._isScared:
      target = self._corner

    legal_actions = world.get_legal_actions(self._position)
    best_action = list(sorted(
      legal_actions,
      key=lambda action: manhattan_distance(self._position.apply_action(action), target)
    ))[0]

    self._position = self._position.apply_action(best_action)

