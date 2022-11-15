from __future__ import annotations
from actions import Action
from position import Position
from tile import Tile


MAP_WALL = "#"
MAP_GUM = "."
MAP_SUPER_GUM = "O"
MAP_BLANK = " "

class World:
  @property
  def width(self) -> int:
    return len(self.__tiles[0])

  @property
  def height(self) -> int:
    return len(self.__tiles)

  @property
  def walls(self) -> list[Position]:
    return self.__walls

  def __init__(self, tiles: list[list[Tile]]) -> None:
    self.__tiles = tiles
    self.__walls = self.__getWalls()

  def __getitem__(self, index: int) -> list[Tile]:
    return self.__tiles[index]

  def get_legal_actions(self, position: Position) -> list[Action]:
    return list(filter(
      lambda action: not self.__isWall(position.apply_action(action)),
      Action.as_list()
    ))

  def isInBounds(self, position: Position) -> bool:
    return 0 <= position.row and position.row < self.width \
      and 0 <= position.column and position.column < self.height

  def __isWall(self, position: Position) -> bool:
    return 0 <= position.row and position.row < len(self.__tiles) \
      and 0 <= position.column and position.column < len(self.__tiles[0]) \
      and self.__tiles[position.row][position.column].isWall

  def __getWalls(self) -> list[Position]:
    positions = []
    for row in range(len(self.__tiles)):
      for col in range(len(self.__tiles[row])):
        if self.__tiles[row][col].isWall:
          positions.append(Position(row, col))
    return positions

  def getGums(self) -> list[Position]:
    positions = []
    for row in range(len(self.__tiles)):
      for col in range(len(self.__tiles[row])):
        if self.__tiles[row][col].isGum or self.__tiles[row][col].isSuperGum:
          positions.append(Position(row, col))
    return positions

  @staticmethod
  def parseArray(world: str) -> World:
    str_map = world.strip().split("\n")
    tiles: list[list[Tile]] = [[] for _ in str_map]

    row = 0
    for line in str_map:
      for item in line:
        if item == MAP_WALL:
          tiles[row].append(Tile(isWall=True))
        elif item == MAP_GUM:
          tiles[row].append(Tile(isGum=True))
        elif item == MAP_SUPER_GUM:
          tiles[row].append(Tile(isSuperGum=True))
        elif item == MAP_BLANK:
          tiles[row].append(Tile(isEmpty=True))
        else: raise Exception("Invalid item in map !")
      row += 1

    return World(tiles)