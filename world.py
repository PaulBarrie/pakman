from __future__ import annotations
from tile import Tile


MAP_WALL = "#"
MAP_GUM = "."
MAP_SUPER_GUM = "O"

class World:
  def tiles(self) -> list[list[Tile]]:
    return self.__tiles

  def __init__(self, tiles: list[list[Tile]]) -> None:
    self.__tiles = tiles

  def __getitem__(self, index: int) -> list[Tile]:
    return self.__tiles[index]

  @staticmethod
  def parseArray(world: str) -> World:
    str_map = world.strip().split("\n")
    tiles: list[list[Tile]] = [[] for x in str_map]

    row = 0
    for line in str_map:
      col = 0
      for item in line:
        if item == MAP_WALL:
          tiles[row][col] = Tile(isWall=True)
        elif item == MAP_GUM:
          tiles[row][col] = Tile(isGum=True)
        elif item == MAP_SUPER_GUM:
          tiles[row][col] = Tile(isSuperGum=True)
        else: raise Exception("Invalid item in map !")
        col += 1
      row += 1

    return World(tiles)