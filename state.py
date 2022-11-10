from __future__ import annotations
from position import Position
from actions import Action, Direction
from utils import aStarSearch



def getTarget(position: Position, gums: list[Position], walls: list[Position]) -> int:
  directions = aStarSearch(position, gums, walls)
  if directions is None: return 0

  target = directions[0]
  if target == Direction.NORTH: return 1
  elif target == Direction.WEST: return 2
  elif target == Direction.SOUTH: return 3
  else: return 4

MAX_STEPS = 4
def getThreat(position: Position, pacman: Position, walls: list[Position]) -> Direction:
  directions = aStarSearch(position, [pacman], walls, MAX_STEPS)
  if directions is None: return None
  return directions[-1].getReverse()

# class State:
#   def value(self) -> tuple[bool, bool, bool, bool, int, bool, bool, bool, bool, bool]:
#     return self.__value

#   def __init__(self, value: tuple[bool, bool, bool, bool, int, bool, bool, bool, bool, bool]) -> None:
#     self.__value = value

#   def __eq__(self, __o: object) -> bool:
#     return isinstance(__o, State) and self.__value == __o.value

#   def __hash__(self) -> int:
#     return hash(self.__value)

#   def __repr__(self) -> str:
#     return f"walls: N{self.__value[0]} W{self.__value[1]} S{self.__value[2]} E{self.__value[3]}\n" + \
#       f"target: {self.__value[4]}\n" + \
#       f"threats:  N{self.__value[5]} W{self.__value[6]} S{self.__value[7]} E{self.__value[8]}\n" + \
#       f"is trapped ? {self.__value[9]}"

State = tuple[bool, bool, bool, bool, int, bool, bool, bool, bool, bool]

## STATE
## north wall - west wall - south wall - east wall (booleans)
## direction of next target (int)
## threat north - threat west - threat south - threat east (booleans)
## trapped (boolean)
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
    threatS = searchRes == Direction.SOUTH
    threatE = searchRes == Direction.EAST

  trapped = threatN and threatW and threatS and threatE
  return (wallN, wallW, wallS, wallE, target, threatN, threatW, threatS, threatE, trapped)
