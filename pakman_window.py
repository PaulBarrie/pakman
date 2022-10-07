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
        self.__agents = (agent, environment.blinky, environment.inky, environment.pinky, environment.clyde)
        self.__current_agent_index = 0

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
        self.__gums.draw()
        self.__ghosts.draw()
        self.__pacman.draw()

    def on_update(self, delta_time):
        moving_agent = self.__agents[self.__current_agent_index]

        if isinstance(moving_agent, Ghost):
            print("here")
            moving_agent.step(self.__environment.walls, self.__agent)
            spr = self.__ghosts[self.__current_agent_index - 1]
            spr.center_x, spr.center_y = self.position_to_xy(moving_agent.position)

            self.__current_agent_index = (self.__current_agent_index + 1) % len(self.__agents)
            return

        # still alive and uneaten gums left on the map
        if self.__agent.lives > 0 and len(self.__environment.gums) > 0:
            self.__agent.step()
            print(self.__agent.position.row, self.__agent.position.column)
        self.__pacman.center_x, self.__pacman.center_y = self.position_to_xy(self.__agent.position)
        self.__current_agent_index = (self.__current_agent_index + 1) % len(self.__agents)
        # else:
        #     # self.__sound.play()
        #     self.__agent.reset()
        #     self.__iteration += 1

        #     self.__player.center_x, self.__player.center_y = \
        #         self.state_to_xy(self.__agent.state)