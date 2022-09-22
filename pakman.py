import arcade

SPRITE_SCALE = 0.33
SPRITE_SIZE = round(128 * SPRITE_SCALE)

class Pakman(arcade.Window):
    def __init__(self, agent):
        super().__init__(SPRITE_SIZE * agent.environment.width,
                         SPRITE_SIZE * agent.environment.height, "Pakman")
        self.__agent = agent
