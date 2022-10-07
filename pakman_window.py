import arcade
from core_game.pakman import Pakman

from core_game.position import Position
from environment.environment import Environment

SPRITE_SCALE = 0.25
SPRITE_SIZE = round(128 * SPRITE_SCALE)

GUM_SCALE = 0.5


class PakmanWindow(arcade.Window):
    def __init__(self, environment: Environment, agent: Pakman):
        super().__init__(SPRITE_SIZE * environment.width,
                         SPRITE_SIZE * environment.height, "Pakman")
        self.__agent = agent
        self.__environment = environment

    def setup(self):
        self.__walls = arcade.SpriteList()
        self.__ghosts = arcade.SpriteList()
        self.__gums = arcade.SpriteList()

        for wall in self.__environment.walls:
            sprite = arcade.Sprite(':resources:images/tiles/boxCrate.png', SPRITE_SCALE)
            sprite.center_x, sprite.center_y = self.position_to_xy(wall)
            self.__walls.append(sprite)

        sprite = arcade.Sprite('static/blinky.png')
        sprite.center_x, sprite.center_y = self.position_to_xy(self.__environment.blinky.position)
        self.__ghosts.append(sprite)

        sprite = arcade.Sprite('static/inky.png')
        sprite.center_x, sprite.center_y = self.position_to_xy(self.__environment.inky.position)
        self.__ghosts.append(sprite)

        sprite = arcade.Sprite('static/pinky.png')
        sprite.center_x, sprite.center_y = self.position_to_xy(self.__environment.pinky.position)
        self.__ghosts.append(sprite)

        sprite = arcade.Sprite('static/clyde.png')
        sprite.center_x, sprite.center_y = self.position_to_xy(self.__environment.clyde.position)
        self.__ghosts.append(sprite)

        for gum in self.__environment.gums:
            sprite = arcade.Sprite('static/gum.png', GUM_SCALE)
            sprite.center_x, sprite.center_y = self.position_to_xy(gum)
            self.__gums.append(sprite)

        self.__pacman = arcade.Sprite('static/pacmanR.png')
        self.__pacman.center_x, self.__pacman.center_y \
                                = self.position_to_xy(self.__agent.position)

    # def state_to_xy(self, state):
    #     return (state[1] + 0.5) * SPRITE_SIZE,\
    #            (self.__environment.height - state[0] - 0.5) * SPRITE_SIZE

    def position_to_xy(self, position: Position) -> tuple[int, int]:
        return (position.column + 0.5) * SPRITE_SIZE, \
            (self.__environment.height - position.row - 0.5) * SPRITE_SIZE

    def on_draw(self):
        arcade.start_render()
        self.__walls.draw()
        self.__ghosts.draw()
        self.__pacman.draw()
        self.__gums.draw()
