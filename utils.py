from collections import deque
from typing import Deque
from actions import Action, Direction
from position import Position


def manhattan_distance(position1: Position, position2: Position) -> int:
  return abs(position1.row - position2.row) + abs(position1.column - position2.column)

def aStarSearch(start: Position, targets: list[Position], obstacles: list[Position], maxDist: int = None) -> list[Direction]:
  frontier: Deque[tuple[Position, list[Direction], int]] = deque()
  explored: set[Position] = set()
  frontier.append((start, [], 0))

  while(len(frontier)):
    pos, directions, dist = frontier.pop()
    if pos in explored: continue

    explored.add(pos)
    if pos in targets:
      return directions

    if maxDist is not None and dist == maxDist:
      continue

    for action in Action.as_list():
      next_pos = pos.apply_action(action)
      direction = action.to_direction()
      if next_pos not in obstacles:
        frontier.append((next_pos, directions + [direction], dist + 1))
  return None
