from position import Position


def manhattan_distance(position1: Position, position2: Position) -> int:
  return abs(position1.row - position2.row) + abs(position1.column - position2.column)