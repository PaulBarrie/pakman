class Tile:
  @property
  def isWall(self) -> bool:
    return self.__isWall

  @property
  def isGum(self) -> bool:
    return self.__isGum

  @property
  def isSuperGum(self) -> bool:
    return self.__isSuperGum

  @property
  def isEmpty(self) -> bool:
    return self.__isEmpty

  def __init__(self, isWall = False, isGum = False, isSuperGum = False, isEmpty = False) -> None:
    self.__isWall = isWall
    self.__isGum = isGum
    self.__isSuperGum = isSuperGum
    self.__isEmpty = isEmpty

  def empty(self) -> None:
    if self.__isGum:
      self.__isGum = False
    if self.__isSuperGum:
      self.__isSuperGum = False
    if not self.__isWall:
      self.__isEmpty = True