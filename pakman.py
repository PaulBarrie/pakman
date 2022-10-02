import arcade

SPRITE_SCALE = 0.33
SPRITE_SIZE = round(128 * SPRITE_SCALE)


class Pakman(arcade.Window):
    def __init__(self, agent):
        super().__init__(SPRITE_SIZE * agent.environment.width,
                         SPRITE_SIZE * agent.environment.height, "Pakman")
        self.__agent = agent

    def setup(self):
        self.__walls = arcade.SpriteList()
        for wall in self.__agent.environment.walls:
            sprite = arcade.Sprite(':resources:images/tiles/boxCrate.png', SPRITE_SCALE)
            sprite.center_x, sprite.center_y = self.state_to_xy(wall)
            self.__walls.append(sprite)

    def state_to_xy(self, state):
        return (state[1] + 0.5) * SPRITE_SIZE,\
               (self.__agent.environment.height - state[0] - 0.5) * SPRITE_SIZE

    def on_draw(self):
        arcade.start_render()
        self.__walls.draw()
