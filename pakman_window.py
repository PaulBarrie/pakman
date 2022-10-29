import arcade
from agents.qtable_pakman import QtablePakman
from core_game.ghost import Ghost
from core_game.pakman import Pakman

from core_game.position import Position
from environment.environment import Environment
from environment.state import State
from pakman_game import PakmanGame

SPRITE_SCALE = 0.25
SPRITE_SIZE = round(128 * SPRITE_SCALE)

GUM_SCALE = 0.5


class PakmanWindow(arcade.Window):
    def __init__(self, environment: Environment, agent: Pakman):
        super().__init__(SPRITE_SIZE * environment.width,
                         SPRITE_SIZE * environment.height, "Pakman")
        self.__game = PakmanGame(environment, agent)

    def setup(self):
        self.__walls = arcade.SpriteList()
        self.__blinky = arcade.Sprite()
        self.__inky = arcade.Sprite()
        self.__pinky = arcade.Sprite()
        self.__clyde = arcade.Sprite()
        self.__gums = arcade.SpriteList()

        for wall in self.__game.environment.walls:
            sprite = arcade.Sprite(':resources:images/tiles/boxCrate.png', SPRITE_SCALE)
            sprite.center_x, sprite.center_y = self.position_to_xy(wall)
            self.__walls.append(sprite)

        sprite = arcade.Sprite('static/blinky.png')
        sprite.center_x, sprite.center_y = self.position_to_xy(self.__game.environment.blinky.position)
        self.__blinky = sprite

        sprite = arcade.Sprite('static/inky.png')
        sprite.center_x, sprite.center_y = self.position_to_xy(self.__game.environment.inky.position)
        self.__inky = sprite

        sprite = arcade.Sprite('static/pinky.png')
        sprite.center_x, sprite.center_y = self.position_to_xy(self.__game.environment.pinky.position)
        self.__pinky = sprite

        sprite = arcade.Sprite('static/clyde.png')
        sprite.center_x, sprite.center_y = self.position_to_xy(self.__game.environment.clyde.position)
        self.__clyde = sprite

        for gum in self.__game.environment.gums:
            sprite = arcade.Sprite('static/gum.png', GUM_SCALE)
            sprite.center_x, sprite.center_y = self.position_to_xy(gum)
            self.__gums.append(sprite)

        self.__pacman = arcade.Sprite('static/pacmanR.png')
        self.__pacman.center_x, self.__pacman.center_y \
                                = self.position_to_xy(self.__game.agent.position)

    def position_to_xy(self, position: Position) -> tuple[int, int]:
        return (position.column + 0.5) * SPRITE_SIZE, \
            (self.__game.environment.height - position.row - 0.5) * SPRITE_SIZE

    def on_draw(self):
        arcade.start_render()
        self.__walls.draw()

        self.__gums.clear()
        for gum in self.__game.environment.gums:
            sprite = arcade.Sprite('static/gum.png', GUM_SCALE)
            sprite.center_x, sprite.center_y = self.position_to_xy(gum)
            self.__gums.append(sprite)
        self.__gums.draw()

        self.__blinky.draw()
        self.__inky.draw()
        self.__pinky.draw()
        self.__clyde.draw()
        self.__pacman.draw()
        arcade.draw_text(f'#{self.__game.iteration} Score: {self.__game.agent.score} Lives: {self.__game.agent.lives} T°C: {round(self.__game.agent.temperature * 100, 2)}',
                         10, 10,
                         arcade.csscolor.WHITE, 20)

    def on_update(self, delta_time):       
        self.__game.update()
        self.__blinky.center_x, self.__blinky.center_y = self.position_to_xy(self.__game.environment.blinky.position)
        self.__inky.center_x, self.__inky.center_y = self.position_to_xy(self.__game.environment.inky.position)
        self.__pinky.center_x, self.__pinky.center_y = self.position_to_xy(self.__game.environment.pinky.position)
        self.__clyde.center_x, self.__clyde.center_y = self.position_to_xy(self.__game.environment.clyde.position)
        self.__pacman.center_x, self.__pacman.center_y = self.position_to_xy(self.__game.agent.position)


    def reset(self):
        self.__game.reset()
