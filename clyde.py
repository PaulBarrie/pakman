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
    if self.__isScattering or self.__isScared or manhattan_distance(self.__position, pacman) <= 4:
      target = self.__corner

    legal_actions = world.get_legal_actions(self.__position)
    best_action = list(sorted(
      legal_actions,
      key=lambda action: manhattan_distance(self.__position.apply_action(action), target)
    ))[0]

    self.__position = self.__position.apply_action(best_action)