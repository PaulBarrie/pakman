import os
import arcade
from matplotlib import pyplot as plt
from actions import Direction
from config import GAME1, GAME1_NO_GHOSTS
from game import Game
from pacman import Pacman
from position import Position
from qtable_pacman import QtablePacman
from state import State, compute_state
from world import World

SAVE_FILE = "qtable.dat"

SPRITE_SCALE = 0.25
SPRITE_SIZE = round(128 * SPRITE_SCALE)
GUM_SCALE = 0.5
GHOST_SPRITES = ['static/blinky.png', 'static/pinky.png', 'static/inky.png', 'static/clyde.png']

# pacman texture ids
PACMAN_UP = 0
PACMAN_LEFT = 1
PACMAN_DOWN = 2
PACMAN_RIGHT = 3

class PacmanSprite(arcade.Sprite):
  def __init__(self, pacman: Pacman) -> None:
    super().__init__()
    self.__pacman = pacman

    self.append_texture(arcade.load_texture('static/pacmanU.png'))
    self.append_texture(arcade.load_texture('static/pacmanL.png'))
    self.append_texture(arcade.load_texture('static/pacmanD.png'))
    self.append_texture(arcade.load_texture('static/pacmanR.png'))
    self.texture = self.textures[PACMAN_LEFT]

  def update(self):
    if self.__pacman.direction == Direction.NORTH:
      self.texture = self.textures[PACMAN_UP]
    elif self.__pacman.direction == Direction.WEST:
      self.texture = self.textures[PACMAN_LEFT]
    elif self.__pacman.direction == Direction.SOUTH:
      self.texture = self.textures[PACMAN_DOWN]
    else: self.texture = self.textures[PACMAN_RIGHT]
    

class PacmanGUI(arcade.Window):
  def __init__(self, game: Game, maxRounds = 5):
    super().__init__(
      SPRITE_SIZE * game.world.width,
      SPRITE_SIZE * game.world.height, "Pakman"
    )
    self.__game = game
    self.__maxRounds = maxRounds
    self.__rounds = 0

  def setup(self):
      self.__walls = arcade.SpriteList()
      self.__ghosts = arcade.SpriteList()
      self.__gums = arcade.SpriteList()

      for wall in self.__game.world.walls:
        sprite = arcade.Sprite(':resources:images/tiles/boxCrate.png', SPRITE_SCALE)
        sprite.center_x, sprite.center_y = self.position_to_xy(wall)
        self.__walls.append(sprite)

      for i in range(len(self.__game.ghosts)):
        sprite = arcade.Sprite(GHOST_SPRITES[i])
        sprite.center_x, sprite.center_y = self.position_to_xy(self.__game.ghosts[i].position)
        self.__ghosts.append(sprite)

      for gum in self.__game.world.getGums():
        sprite = arcade.Sprite('static/gum.png', GUM_SCALE)
        sprite.center_x, sprite.center_y = self.position_to_xy(gum)
        self.__gums.append(sprite)

      self.__pacman = PacmanSprite(self.__game.pacman)
      self.__pacman.center_x, self.__pacman.center_y = \
        self.position_to_xy(self.__game.pacman.position)

  def position_to_xy(self, position: Position) -> tuple[int, int]:
    return (position.column + 0.5) * SPRITE_SIZE, \
      (self.__game.world.height - position.row - 0.5) * SPRITE_SIZE

  def on_draw(self):
    arcade.start_render()

    self.__walls.draw()
    self.__gums.clear()
    for gum in self.__game.world.getGums():
      sprite = arcade.Sprite('static/gum.png', GUM_SCALE)
      sprite.center_x, sprite.center_y = self.position_to_xy(gum)
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
    if self.__game.isGameOver or self.__game.moves >= 200:
      self.__game.setNextRound()
      self.__rounds += 1
    
    if self.__rounds == self.__maxRounds:
      return

    self.__game.move()

    for i in range(len(self.__ghosts)):
      self.__ghosts[i].center_x, self.__ghosts[i].center_y = \
        self.position_to_xy(self.__game.ghosts[i].position)
    self.__pacman.update()
    self.__pacman.center_x, self.__pacman.center_y = self.position_to_xy(self.__game.pacman.position)

def pFactory(config, world: World, qtable = None) -> Pacman:
  position = position=Position(config["pacman"]["position"][0], config["pacman"]["position"][1])

  ghosts = [
    Position(config["blinky"]["position"][0], config["blinky"]["position"][1]),
    Position(config["pinky"]["position"][0], config["pinky"]["position"][1]),
    Position(config["inky"]["position"][0], config["inky"]["position"][1]),
    Position(config["clyde"]["position"][0], config["clyde"]["position"][1])
  ]
  # ghosts = []
  state = compute_state(
    pacman_position=position,
    ghost_positions=ghosts,
    gum_positions=world.getGums(),
    wall_positions=world.walls
  )

  return QtablePacman(
    position=position,
    state=state,
    qtable=qtable
  )


if __name__ == "__main__":
  game = Game(GAME1, pacmanFactory=pFactory)

  if os.path.exists(SAVE_FILE):
    game.pacman.load(SAVE_FILE)

  gui = PacmanGUI(game)
  gui.setup()
  arcade.run()

  plt.plot(game.pacman.history)
  plt.show()