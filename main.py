from pakman import Pakman
from environment.environment import Environment
from agent import Agent
import maps

if __name__ == '__main__':
    environment = Environment(maps.GAME1)
    agent = Agent(environment)
    pakman = Pakman(agent)
