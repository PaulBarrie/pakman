from __future__ import annotations
from position import Position
from actions import Action, Direction
from utils import aStarSearch, manhattan_distance



def getTarget(position: Position, gums: list[Position], walls: list[Position]) -> int:
  if len(gums) == 0: return 0

  directions = aStarSearch(position, gums, walls)
  if directions is None: return 0

  target = directions[0]
  if target == Direction.NORTH: return 1
  elif target == Direction.WEST: return 2
  elif target == Direction.SOUTH: return 3
  else: return 4

MAX_STEPS = 2
def getThreat(position: Position, pacman: Position, walls: list[Position]) -> Direction:
  directions = aStarSearch(position, [pacman], walls, MAX_STEPS)
  if directions is None: return None
  return directions[-1].getReverse()

# returns a tuple of 4 booleans, 1 for each tile directly next to the position,
# indicating whether a target is in a tile
# order : North, West, South, West
def getShortRangeRadar(position: Position, targets: list[Position]) -> tuple[bool, bool, bool, bool]:
  return tuple(map(
    lambda action: position.apply_action(action) in targets,
    Action.as_list()
  ))

# returns a tuple of 4 booleans and an int,
# the 4 booleans indicate where the closest target is relative to the position
# value: a combination of the 4 cardinal points, i.e N or W or SE or NE, etc.
# order: North, West, South, East
# the int indicates a distance from 1 to 3, 3 meaning there are 3 tiles OR MORE between the position and the target
def getLongRangeRadar(position: Position, targets: list[Position]) -> tuple[bool, bool, bool, bool, int]:
  if len(targets) == 0:
    return (False, False, False, False, 1)

  sortedTargets = list(sorted(
    targets,
    key=lambda targetPosition: manhattan_distance(position, targetPosition)
  ))
  
  closestTargetPosition = sortedTargets[0]
  dist = manhattan_distance(closestTargetPosition, position)
  dist = dist if dist <= 3 else 3

  return (
    closestTargetPosition.row < position.row,
    closestTargetPosition.column < position.column,
    closestTargetPosition.row > position.row,
    closestTargetPosition.column > position.column,
    dist
  )

MAX_RANGE = 4
def getAreaRadar(position: Position, threats: list[Position]) -> tuple[bool, bool, bool, bool, bool, bool, bool, bool]:
  threatN = False
  threatW = False
  threatS = False
  threatE = False
  threatNW = False
  threatNE = False
  threatSW = False
  threatSE = False

  directThreats = list(filter(lambda threat: manhattan_distance(position, threat) <= MAX_RANGE, threats))
  for t in directThreats:
    if t.row == position.row:
      threatW = t.column < position.column
      threatE = t.column > position.column
      continue

    if t.column == position.column:
      threatN = t.row < position.row
      threatS = t.row > position.row
      continue

    if t.row < position.row:
      threatNW = t.column < position.column
      threatNE = t.column > position.column
      continue

    threatSW = t.column < position.column
    threatSE = t.column > position.column

  return (threatN, threatW, threatS, threatE, threatNW, threatNE, threatSW, threatSE)


## STATE
## north wall - west wall - south wall - east wall (booleans)
## direction of next target (int)
## threat north - threat west - threat south - threat east (booleans)
## trapped (boolean)

State = tuple[bool, bool, bool, bool, int, bool, bool, bool, bool, bool]

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

# ORIGINAL IMPLEMENTATION

# State = tuple[bool, bool, bool, bool, bool, bool, bool, bool, int, bool, bool, bool, bool, bool, bool, bool, bool]

# def compute_state(
#   ghost_positions: list[Position], 
#   pacman_position: Position, 
#   gum_positions: list[Position], 
#   wall_positions: list[Position]
# ) -> State:

#   wallN, wallW, wallS, wallE = getShortRangeRadar(pacman_position, wall_positions)
#   gumN, gumW, gumS, gumE, gumDist = getLongRangeRadar(pacman_position, gum_positions)
#   threatN, threatW, threatS, threatE, threatNW, threatNE, threatSW , threatSE = \
#     getAreaRadar(pacman_position, ghost_positions)

#   return (wallN, wallW, wallS, wallE, gumN, gumW, gumS, gumE, gumDist, threatN, threatW, threatS, threatE, threatNW, threatNE, threatSW, threatSE)
