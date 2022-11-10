from typing import Any, Callable
from actions import Action
from blinky import Blinky
from clyde import Clyde
from ghost import Ghost
from inky import Inky
from pacman import Pacman
from pinky import Pinky
from position import Position
from state import State, compute_state
from world import World


DEFAULT_REWARD = -50
GUM_REWARD = 100
GHOST_REWARD = -500
WALL_REWARD = -1000
WIN_REWARD = 1000
AGENTS = 5

class Game:
  @property
  def world(self) -> World:
    return self.__world
  
  @property
  def ghosts(self) -> list[Ghost]:
    return self.__ghosts

  @property
  def pacman(self) -> Pacman:
    return self.__pacman

  @property
  def moves(self) -> int:
    return self.__moves

  @property
  def rounds(self) -> int:
    return self.__rounds

  @property
  def isGameOver(self) -> bool:
    return self.__isGameOver

  # pass params
  # and a pacman factory -> it can create, from a config and a world,
  # an instance of QtablePacman or any other subclass of Pacman !
  def __init__(self, config, pacmanFactory: Callable[[Any, World, Any], Pacman], moves=0, rounds=0, isGameOver=False) -> None:
    self.__config = config
    self.__pacmanFactory = pacmanFactory

    self.__world = self.__generateWorld(config)
    self.__ghosts = self.__generateGhosts(config)
    self.__pacman = self.__pacmanFactory(config, self.__world)
    self.__moves = moves
    self.__rounds = rounds
    self.__isGameOver = isGameOver
    self.__internalMovesCount = 0
    self.__pacmanRespawnLocation = Position(
      config["pacman"]["position"][0], 
      config["pacman"]["position"][1]
    )

  def move(self) -> None:
    if len(self.__ghosts) and self.__internalMovesCount < AGENTS - 1:
      currentGhost = self.__ghosts[self.__internalMovesCount]
      currentGhost.move(self.__world, self.__pacman)
      if currentGhost.position == self.__pacman.position:
        self.__pacman.die(self.__pacmanRespawnLocation)
        self.resetGhosts()
    else:
      self.__pacman.step(self)
    self.__internalMovesCount = (self.__internalMovesCount + 1) % AGENTS

  # never call this method in a window / context
  # called by Pacman when moving
  # returns a tuple containing
  #  - the new state
  #  - the reward
  #  - the next position 
  def do(self, position: Position, action: Action, state: State) -> tuple[State, float, Position]:
    # for ghost in self.__ghosts:
    #   ghost.move(self.__world, self.__pacman)
    self.__moves += 1

    next_position = position.apply_action(action)

    if next_position in self.__getGhostPositions():
      # print("Pacman died !")
      self.__pacman.die(self.__pacmanRespawnLocation)
      self.resetGhosts()
      resetState = compute_state(
        self.__getGhostPositions(), 
        self.__pacmanRespawnLocation, 
        self.__world.getGums(), 
        self.__world.walls
      )

      if self.__pacman.lives <= 0:
        self.__isGameOver = True
      return (resetState, GHOST_REWARD, self.__pacmanRespawnLocation)

    pacmanRow = next_position.row
    pacmanColumn = next_position.column
    targetTile = self.__world[pacmanRow][pacmanColumn]

    ## special logic when a gum is eaten
    if targetTile.isGum or targetTile.isSuperGum:
      # print("Pacman ate a gum !")
      targetTile.empty()
      nextState = compute_state(
        self.__getGhostPositions(), 
        self.__pacman.position, 
        self.__world.getGums(), 
        self.__world.walls
      )

      reward = GUM_REWARD
      # all gums were eaten
      if len(self.__world.getGums()) == 0:
        reward = WIN_REWARD
        self.__isGameOver = True
      return (nextState, reward, next_position)

    ## pacman does not move but gets a bump on the head !
    if targetTile.isWall:
      # print("Pacman bump ots head on a wall !")
      return (state, WALL_REWARD, self.__pacman.position)

    nextState = compute_state(
      self.__getGhostPositions(), 
      self.__pacman.position, 
      self.__world.getGums(), 
      self.__world.walls
    )
    if targetTile.isEmpty:
      # print("Pacman moved !")
      return (nextState, DEFAULT_REWARD, next_position)

    raise Exception("Invalid move or state")

  def resetGhosts(self) -> None:
    self.__ghosts = self.__generateGhosts(self.__config)

  def setNextRound(self) -> None:
    self.resetGhosts()
    # reset the world before resetting Pacman !
    self.__world = self.__generateWorld(self.__config)
    self.__pacman = self.__pacmanFactory(self.__config, self.__world, self.__pacman.qtable)
    self.__moves = 0
    self.__rounds += 1
    self.__isGameOver = False

  def __generateWorld(self, config) -> World:
    return World.parseArray(config["strMap"])

  def __generateGhosts(self, config) -> list[Ghost]:
    if not config.get("blinky") or not config.get("pinky") or not config.get("inky") or not config.get("clyde"):
      return []

    blinky = Blinky(
      position=Position(config["blinky"]["position"][0], config["blinky"]["position"][1]),
      corner=Position(config["blinky"]["corner"][0], config["blinky"]["corner"][1])
    )
    pinky = Pinky(
      position=Position(config["pinky"]["position"][0], config["pinky"]["position"][1]),
      corner=Position(config["pinky"]["corner"][0], config["pinky"]["corner"][1])
    )
    inky = Inky(
      position=Position(config["inky"]["position"][0], config["inky"]["position"][1]),
      corner=Position(config["inky"]["corner"][0], config["inky"]["corner"][1]),
      blinky=blinky
    )
    clyde = Clyde(
      position=Position(config["clyde"]["position"][0], config["clyde"]["position"][1]),
      corner=Position(config["clyde"]["corner"][0], config["clyde"]["corner"][1])
    )
    return [blinky, pinky, inky, clyde]

  def __getGhostPositions(self) -> list[Position]:
    return list(map(lambda g: g.position, self.__ghosts))

