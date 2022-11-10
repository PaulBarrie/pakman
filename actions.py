from __future__ import annotations
from enum import Enum



class Direction(str, Enum):
  NORTH = "North"
  SOUTH = "South"
  WEST = "West"
  EAST = "East"

  def is_reverse(self, other_direction: Direction) -> bool:
    return (self == Direction.NORTH and other_direction == Direction.SOUTH) \
      or (self == Direction.SOUTH and other_direction == Direction.NORTH) \
      or (self == Direction.WEST and other_direction == Direction.EAST) \
      or (self == Direction.EAST and other_direction == Direction.WEST)

  def getReverse(self) -> Direction:
    if self == Direction.NORTH: return Direction.SOUTH
    elif self == Direction.WEST: return Direction.EAST
    elif self == Direction.SOUTH: return Direction.NORTH
    else: return Direction.WEST

  @staticmethod
  def as_list() -> list[Direction]:
    return [Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST]


        
class Action(tuple[int, int], Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def to_direction(self) -> Direction:
        if self == Action.UP:
            return Direction.NORTH
        if self == Action.DOWN:
            return Direction.SOUTH
        if self == Action.LEFT:
            return Direction.WEST
        return Direction.EAST

    @staticmethod
    def from_direction(direction: Direction) -> Action:
        if direction == Direction.NORTH:
            return Action.UP
        if direction == Direction.SOUTH:
            return Action.DOWN
        if direction == Direction.WEST:
            return Action.LEFT
        if direction == Direction.EAST:
            return Action.RIGHT
        
        raise ValueError("Invalid direction")


    @staticmethod
    def as_list() -> list[Action]:
        return [Action.UP, Action.LEFT, Action.DOWN, Action.RIGHT]

    # @staticmethod
    # def asReverseList() -> list[Action]:
    #     return [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT, Action.LEFT, Action.DOWN]