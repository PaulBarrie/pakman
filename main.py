from pakman import Pakman
from environment.environment import Environment
from agent import Agent
import maps
import arcade

if __name__ == '__main__':
    environment = Environment(maps.GAME2)
    agent = Agent(environment)
    pakman = Pakman(agent)
    pakman.setup()
    arcade.run()
