from __future__ import annotations
from actions import Action
from position import Position
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

  def get_legal_actions(self, position: Position) -> list[Action]:
    return list(filter(
      lambda action: not self.__is_wall(position.apply_action(action)),
      Action.as_list()
    ))

  def __is_wall(self, position: Position) -> bool:
    return 0 <= position.row and position.row < len(self.__tiles) \
      and 0 <= position.column and position.column < len(self.__tiles[0]) \
      and self.__tiles[position.row][position.column].isWall

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