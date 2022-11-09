# from __future__ import annotations
# from position import Position
# from actions import Action
# from metrics import *


# class ShortRangeRadar:
#     @property
#     def north(self) -> bool:
#         return self.__north

#     @property
#     def south(self) -> bool:
#         return self.__south

#     @property
#     def west(self) -> bool:
#         return self.__west

#     @property
#     def east(self) -> bool:
#         return self.__east

#     def __init__(self, north: bool, south: bool, west: bool, east: bool) -> None:
#         self.__north = north
#         self.__south = south
#         self.__west = west
#         self.__east = east

#     @staticmethod
#     def compute_radar(position: Position, targets: list[Position]) -> ShortRangeRadar:
#         north_position = position.apply_action(Action.UP)
#         south_position = position.apply_action(Action.DOWN)
#         west_position = position.apply_action(Action.LEFT)
#         east_position = position.apply_action(Action.RIGHT)

#         return ShortRangeRadar(
#             north_position in targets,
#             south_position in targets,
#             west_position in targets,
#             east_position in targets
#         )

#     def __eq__(self, __o: object) -> bool:
#         return isinstance(__o, ShortRangeRadar) \
#             and self.__north == __o.north \
#             and self.__south == __o.south \
#             and self.__west == __o.west \
#             and self.__east == __o.east

#     def __hash__(self) -> int:
#         return hash((self.__north, self.__south, self.__west, self.__east))


# class LongRangeRadar:
#     """
#         Directions
#             NE  | NO
#                 |
#         ----------------
#             SE  | SO
#                 |
#     """
#     @property
#     def north(self) -> bool:
#         return self.__north
    
#     @property
#     def south(self) -> bool:
#         return self.__south

#     @property
#     def west(self) -> bool:
#         return self.__west

#     @property
#     def east(self) -> bool:
#         return self.__east

#     @property
#     def distance(self) -> Distance:
#         return self.__distance

#     def __init__(self, north, south, west, east, distance: Distance) -> None:
#         self.__north = north
#         self.__south = south
#         self.__west = west
#         self.__east = east
#         self.__distance = distance

#     def __eq__(self, __o: object) -> bool:
#         return isinstance(__o, LongRangeRadar) \
#             and self.__north == __o.north \
#             and self.__south == __o.south \
#             and self.__west == __o.west \
#             and self.__east == __o.east \
#             and self.__distance == __o.distance

#     def __hash__(self) -> int:
#         return hash((self.__north, self.__south, self.__west, self.__east, self.__distance))

#     @staticmethod
#     def compute_radar(pakman_position: Position, targets: list[Position]) -> LongRangeRadar:
#         closest_target_position = list(sorted(
#             targets,
#             key = lambda gp: gp.get_distance(pakman_position)
#         ))[0]
#         dist = closest_target_position.get_distance(pakman_position)

#         return LongRangeRadar(
#             closest_target_position.row < pakman_position.row,
#             closest_target_position.row > pakman_position.row,
#             closest_target_position.column < pakman_position.column,
#             closest_target_position.column > pakman_position.column,
#             Distance.int_to_distance(dist)
#         )


# class State:
#     STATE_VAL_SEPARATOR = ""

#     @property
#     def ghost_radar(self) -> LongRangeRadar:
#         return self.__ghost_radar

#     @property
#     def gum_radar(self) -> ShortRangeRadar:
#         return self.__gum_radar
    
#     @property
#     def wall_radar(self) -> ShortRangeRadar:
#         return self.__wall_radar

#     def __init__(
#         self, 
#         ghost_radar: LongRangeRadar, 
#         gum_radar: ShortRangeRadar, 
#         wall_radar: ShortRangeRadar
#     ) -> None:
#         self.__ghost_radar = ghost_radar
#         self.__gum_radar = gum_radar
#         self.__wall_radar = wall_radar

#     @staticmethod
#     def compute_state(
#         ghost_positions: list[Position], 
#         pakman_position: Position, 
#         gum_positions: list[Position], 
#         wall_positions: list[Position]
#     ) -> State:

#         return State(
#             LongRangeRadar.compute_radar(pakman_position, ghost_positions),
#             ShortRangeRadar.compute_radar(pakman_position, gum_positions),
#             ShortRangeRadar.compute_radar(pakman_position, wall_positions)
#         )

#     def __eq__(self, __o: object) -> bool:
#         return isinstance(__o, State) \
#             and self.__ghost_radar == __o.ghost_radar \
#             and self.__gum_radar == __o.gum_radar \
#             and self.__wall_radar == __o.wall_radar

#     def __hash__(self) -> int:
#         return hash(( 
#             hash(self.__gum_radar), 
#             hash(self.__wall_radar), 
#             hash(self.__ghost_radar) 
#         ))

#     def __repr__(self) -> str:
#         ghost_state = self.__state_str(self.__ghost_radar)
#         gum_state = self.__state_str(self.__gum_radar)
#         wall_state = self.__state_str(self.__wall_radar)

#         return f'ghost: {ghost_state}, gums: {gum_state}, walls: {wall_state}'


from __future__ import annotations
from position import Position
from actions import Action, Direction
from utils import aStarSearch


def getTarget(position: Position, gums: list[Position], walls: list[Position]) -> int:
  directions = aStarSearch(position, gums, walls)
  if directions is None: return 0

  target = directions[0];
  if target == Direction.NORTH: return 1
  elif target == Direction.WEST: return 2
  elif target == Direction.SOUTH: return 3
  else: return 4

MAX_STEPS = 6
def getThreat(position: Position, pacman: Position, walls: list[Position]) -> Direction:
  directions = aStarSearch(position, [pacman], walls, MAX_STEPS)
  if directions is None: return None
  return directions[-1].getReverse()

class State:
  def value(self) -> tuple[bool, bool, bool, bool, int, bool, bool, bool, bool, bool]:
    return self.__value

  def __init__(self, value: tuple[bool, bool, bool, bool, int, bool, bool, bool, bool, bool]) -> None:
    self.__value = value

  def __eq__(self, __o: object) -> bool:
    return isinstance(__o, State) and self.__value == __o.value

  def __hash__(self) -> int:
    return hash(self.__value)

  @staticmethod
  def compute_state(
    ghost_positions: list[Position], 
    pacman_position: Position, 
    gum_positions: list[Position], 
    wall_positions: list[Position]
  ) -> State:
    wallN = pacman_position.apply_action(Action.UP) in wall_positions
    wallW = pacman_position.apply_action(Action.LEFT) in wall_positions
    wallS = pacman_position.apply_action(Action.DOWN) in wall_positions
    wallE = pacman_position.apply_action(Action.RIGHT) in wall_positions

    target = getTarget(pacman_position, gum_positions, wall_positions)

    threatN = False
    threatW = False
    threatS = False
    threatE = False

    for gp in ghost_positions:
      searchRes = getThreat(gp, pacman_position, wall_positions)
      threatN = searchRes == Direction.NORTH
      threatW = searchRes == Direction.WEST
      threatWS = searchRes == Direction.SOUTH
      threatE = searchRes == Direction.EAST

    trapped = threatN and threatW and threatS and threatE

    return (wallN, wallW, wallS, wallE, target, threatN, threatW, threatS, threatE)
