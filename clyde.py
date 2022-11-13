from ghost import Ghost
from pacman import Pacman
from position import Position
from utils import manhattan_distance
from world import World


class Clyde(Ghost):
  def __init__(self, position: Position, corner: Position) -> None:
    super().__init__(position=position, corner=corner)

  def move(self, world: World, pacman: Pacman) -> None:
    super().move(world, pacman)

    target = pacman.position
    # target pacman but retreat to corner when getting too close
    if self._isScattering or self._isScared or manhattan_distance(self._position, pacman.position) <= 2:
      target = self._corner

    legal_actions = self._filterMoves(world.get_legal_actions(self._position))
    best_action = list(sorted(
      legal_actions,
      key=lambda action: manhattan_distance(self._position.apply_action(action), target)
    ))[0]

    self._position = self._position.apply_action(best_action)
    self._direction = best_action.to_direction()