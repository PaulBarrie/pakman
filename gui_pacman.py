import os
import arcade
from matplotlib import pyplot as plt
from actions import Direction
from config import GAME1, GAME1_NO_GHOSTS, GAME2, GAME2_NO_GHOSTS, GAME3
from game import Game
from pacman import Pacman
from position import Position
from qtable_pacman import QtablePacman
from state import State, compute_state
from world import World

SPRITE_SCALE = 0.25
SPRITE_SIZE = round(128 * SPRITE_SCALE)
GUM_SCALE = 0.5
GHOST_SPRITES = ['static/blinky.png', 'static/inky.png', 'static/pinky.png', 'static/clyde.png']

# pacman texture ids
PACMAN_UP = 0
PACMAN_LEFT = 1
PACMAN_DOWN = 2
PACMAN_RIGHT = 3

def position_to_xy(position: Position, maxHeight: int) -> tuple[int, int]:
  return (position.column + 0.5) * SPRITE_SIZE, \
    (maxHeight - position.row - 0.5) * SPRITE_SIZE

class PacmanSprite(arcade.Sprite):
  @property
  def pacman(self) -> QtablePacman:
    return self.__pacman

  def __init__(self, pacman: Pacman, worldHeight: int) -> None:
    super().__init__()
    self.__pacman = pacman

    self.append_texture(arcade.load_texture('static/pacmanU.png'))
    self.append_texture(arcade.load_texture('static/pacmanL.png'))
    self.append_texture(arcade.load_texture('static/pacmanD.png'))
    self.append_texture(arcade.load_texture('static/pacmanR.png'))
    self.texture = self.textures[PACMAN_LEFT]
    self.__worldHeight = worldHeight
    self.center_x, self.center_y = position_to_xy(pacman.position, worldHeight)

  def update(self):
    self.center_x, self.center_y = \
      position_to_xy(self.__pacman.position, self.__worldHeight)

    if self.__pacman.direction == Direction.NORTH:
      self.texture = self.textures[PACMAN_UP]
    elif self.__pacman.direction == Direction.WEST:
      self.texture = self.textures[PACMAN_LEFT]
    elif self.__pacman.direction == Direction.SOUTH:
      self.texture = self.textures[PACMAN_DOWN]
    else: self.texture = self.textures[PACMAN_RIGHT]
    

class PacmanGUI(arcade.Window):
  def __init__(self, game: Game, maxRounds = 20):
    super().__init__(
      SPRITE_SIZE * game.world.width,
      SPRITE_SIZE * game.world.height, "Pakman"
    )
    self.__game = game
    self.__maxRounds = maxRounds

  def setup(self):
      self.__walls = arcade.SpriteList()
      self.__ghosts = arcade.SpriteList()
      self.__gums = arcade.SpriteList()

      for wall in self.__game.world.walls:
        sprite = arcade.Sprite(':resources:images/tiles/boxCrate.png', SPRITE_SCALE)
        sprite.center_x, sprite.center_y = position_to_xy(wall, self.__game.world.height)
        self.__walls.append(sprite)

      for i in range(len(self.__game.ghosts)):
        sprite = arcade.Sprite(GHOST_SPRITES[i])
        sprite.center_x, sprite.center_y = position_to_xy(self.__game.ghosts[i].position, self.__game.world.height)
        self.__ghosts.append(sprite)

      for gum in self.__game.world.getGums():
        sprite = arcade.Sprite('static/gum.png', GUM_SCALE)
        sprite.center_x, sprite.center_y = position_to_xy(gum, self.__game.world.height)
        self.__gums.append(sprite)

      self.__pacman = PacmanSprite(self.__game.pacman, self.__game.world.height)

  def on_draw(self):
    arcade.start_render()

    self.__walls.draw()
    self.__gums.clear()
    for gum in self.__game.world.getGums():
      sprite = arcade.Sprite('static/gum.png', GUM_SCALE)
      sprite.center_x, sprite.center_y = position_to_xy(gum, self.__game.world.height)
      self.__gums.append(sprite)

    self.__gums.draw()
    self.__ghosts.draw()
    self.__pacman.draw()

    arcade.draw_text(
      f'#{self.__game.rounds} Score: {self.__game.pacman.score} Lives: {self.__game.pacman.lives} T°C: {round(self.__game.pacman.temperature * 100, 2)}',
      10, 10,
      arcade.csscolor.WHITE, 20
    )

  def on_update(self, delta_time):
    if self.__game.rounds >= self.__maxRounds:
      return
    self.__game.move()

    for i in range(len(self.__ghosts)):
      self.__ghosts[i].center_x, self.__ghosts[i].center_y = \
        position_to_xy(self.__game.ghosts[i].position, self.__game.world.height)
    self.__pacman.update()

    if self.__game.moves >= 10000 or self.__game.isGameOver:
      self.__game.setNextRound()
      # self.__game.pacman.heat()

def pFactory(config, world: World, qtable = None, history = None) -> Pacman:
  position = position=Position(config["pacman"]["position"][0], config["pacman"]["position"][1])

  ghosts = []
  if config.get("blinky"):
    print("Blinky config")
    ghosts.append(Position(config["blinky"]["position"][0], config["blinky"]["position"][1]))
  if config.get("pinky") :
    print("Pinky config")
    ghosts.append(Position(config["pinky"]["position"][0], config["pinky"]["position"][1]))
  if config.get("inky"):
    print("Inky config")
    ghosts.append(Position(config["inky"]["position"][0], config["inky"]["position"][1])) 
  if config.get("clyde"):
    print("Clyde config")
    ghosts.append(Position(config["clyde"]["position"][0], config["clyde"]["position"][1]))
    
  state = compute_state(
    pacman_position=position,
    ghost_positions=ghosts,
    gum_positions=world.getGums(),
    wall_positions=world.walls
  )

  return QtablePacman(
    position=position,
    state=state,
    qtable=qtable,
    history=history
  )

SAVE_FILE = "qtable.dat"

def launchGUI():
  game = Game(GAME2_NO_GHOSTS, pacmanFactory=pFactory)

  if os.path.exists(SAVE_FILE):
    game.pacman.load(SAVE_FILE)
  #game.pacman.heat()
  
  gui = PacmanGUI(game)
  gui.setup()
  arcade.run()

  plt.plot(game.pacman.history)
  plt.show()
  if os.path.exists(SAVE_FILE):
    game.pacman.save(SAVE_FILE)