import arcade

SPRITE_SCALE = 0.25
SPRITE_SIZE = round(128 * SPRITE_SCALE)

GUM_SCALE = 0.5


class PakmanWindow(arcade.Window):
    def __init__(self, agent):
        super().__init__(SPRITE_SIZE * agent.environment.width,
                         SPRITE_SIZE * agent.environment.height, "Pakman")
        self.__agent = agent
        self.__iteration = 0

    def setup(self):
        self.__walls = arcade.SpriteList()
        self.__ghosts = arcade.SpriteList()
        self.__gums = arcade.SpriteList()

        for wall in self.__agent.environment.walls:
            sprite = arcade.Sprite(':resources:images/tiles/boxCrate.png', SPRITE_SCALE)
            sprite.center_x, sprite.center_y = self.state_to_xy(wall)
            self.__walls.append(sprite)

        for ghost in self.__agent.environment.ghosts:
            sprite = arcade.Sprite('static/inky.png')
            sprite.center_x, sprite.center_y = self.state_to_xy(ghost)
            self.__ghosts.append(sprite)

        for gum in self.__agent.environment.gums:
            sprite = arcade.Sprite('static/gum.png', GUM_SCALE)
            sprite.center_x, sprite.center_y = self.state_to_xy(gum)
            self.__gums.append(sprite)

        self.__pacman = arcade.Sprite('static/pacmanR.png')
        self.__pacman.center_x, self.__pacman.center_y \
                                = self.state_to_xy(self.__agent.state)

    def state_to_xy(self, state):
        return (state[1] + 0.5) * SPRITE_SIZE,\
               (self.__agent.environment.height - state[0] - 0.5) * SPRITE_SIZE

    def on_draw(self):
        arcade.start_render()
        self.__walls.draw()
        self.__ghosts.draw()
        self.__pacman.draw()
        self.__gums.draw()
        arcade.draw_text(f'#{self.__iteration} Score: {self.__agent.score} T°C: {round(self.__agent.temperature * 100, 2)}',
                         10, 10,
                         arcade.csscolor.WHITE, 20)

    def on_update(self, delta_time: float):
        if len(self.__agent.environment.gums) > 0 :
            self.__agent.step()
        else:
            self.__agent.reset()
            self.__iteration += 1
        self.__pacman.center_x, self.__pacman.center_y \
                                = self.state_to_xy(self.__agent.state)
        self.__gums.clear()
        for gum in self.__agent.environment.gums:
            sprite = arcade.Sprite('static/gum.png', GUM_SCALE)
            sprite.center_x, sprite.center_y = self.state_to_xy(gum)
            self.__gums.append(sprite)
