from agents.qtable_pakman import QtablePakman
from environment.state import State
from pakman_window import PakmanWindow
from environment.environment import Environment
import maps
import arcade

if __name__ == '__main__':
    environment = Environment.from_str_map(maps.GAME2)
    initial_state = State.compute_state(
        environment.ghost_positions, 
        environment.initial_pakman_position,
        environment.gums,
        environment.walls
    )
    agent = QtablePakman(environment.initial_pakman_position, initial_state, environment)
    pakman = PakmanWindow(environment, agent)
    pakman.setup()
    arcade.run()
