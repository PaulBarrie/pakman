from ghost import Ghost
from pacman import Pacman
from position import Position
from utils import manhattan_distance
from world import World


class Pinky(Ghost):
  def __init__(self, position: Position, corner: Position) -> None:
    super().__init__(position=position, corner=corner)

  def move(self, world: World, pacman: Pacman) -> None:
    super().move(world, pacman)

    # target 1 tile in front of Pacman
    target = pacman.position.follow_direction(pacman.direction)
    if self._isScattering or self._isScared:
      target = self._corner

    legal_actions = world.get_legal_actions(self._position)
    best_action = list(sorted(
      legal_actions,
      key=lambda action: manhattan_distance(self._position.apply_action(action), target)
    ))[0]

    self._position = self._position.apply_action(best_action)