import arcade
from core_game.ghost import Ghost
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
        self.__current_agent_index = 0

    def setup(self):
        self.__walls = arcade.SpriteList()
        self.__blinky = arcade.Sprite()
        self.__inky = arcade.Sprite()
        self.__pinky = arcade.Sprite()
        self.__clyde = arcade.Sprite()
        self.__gums = arcade.SpriteList()

        for wall in self.__environment.walls:
            sprite = arcade.Sprite(':resources:images/tiles/boxCrate.png', SPRITE_SCALE)
            sprite.center_x, sprite.center_y = self.position_to_xy(wall)
            self.__walls.append(sprite)

        sprite = arcade.Sprite('static/blinky.png')
        sprite.center_x, sprite.center_y = self.position_to_xy(self.__environment.blinky.position)
        self.__blinky = sprite

        sprite = arcade.Sprite('static/inky.png')
        sprite.center_x, sprite.center_y = self.position_to_xy(self.__environment.inky.position)
        self.__inky = sprite

        sprite = arcade.Sprite('static/pinky.png')
        sprite.center_x, sprite.center_y = self.position_to_xy(self.__environment.pinky.position)
        self.__pinky = sprite

        sprite = arcade.Sprite('static/clyde.png')
        sprite.center_x, sprite.center_y = self.position_to_xy(self.__environment.clyde.position)
        self.__clyde = sprite

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

        self.__gums.clear()
        for gum in self.__environment.gums:
            sprite = arcade.Sprite('static/gum.png', GUM_SCALE)
            sprite.center_x, sprite.center_y = self.position_to_xy(gum)
            self.__gums.append(sprite)
        self.__gums.draw()

        self.__blinky.draw()
        self.__inky.draw()
        self.__pinky.draw()
        self.__clyde.draw()
        self.__pacman.draw()

    def on_update(self, delta_time):          
        if self.__current_agent_index == 1:
            blinky = self.__environment.blinky
            blinky.step(self.__environment.walls, self.__agent)
            self.__blinky.center_x, self.__blinky.center_y = self.position_to_xy(blinky.position)

        elif self.__current_agent_index == 2:
            inky = self.__environment.inky
            inky.step(self.__environment.walls, self.__agent)
            self.__inky.center_x, self.__inky.center_y = self.position_to_xy(inky.position)

        elif self.__current_agent_index == 3:
            pinky = self.__environment.pinky
            pinky.step(self.__environment.walls, self.__agent)
            self.__pinky.center_x, self.__pinky.center_y = self.position_to_xy(pinky.position)

        elif self.__current_agent_index == 4:
            clyde = self.__environment.clyde
            clyde.step(self.__environment.walls, self.__agent)
            self.__clyde.center_x, self.__clyde.center_y = self.position_to_xy(clyde.position)

        else: 
            if self.__agent.lives > 0 and len(self.__environment.gums) > 0:
                self.__agent.step()
                self.__pacman.center_x, self.__pacman.center_y = self.position_to_xy(self.__agent.position)
            else:
                # reset env + pakman
                exit(0)

        self.__current_agent_index = (self.__current_agent_index + 1) % 5