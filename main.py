import os
from agents.qtable_pakman import QtablePakman
from environment.state import State
from pakman_window import PakmanWindow
from environment.environment import Environment
import maps
import arcade
import matplotlib.pyplot as plt

from pakman_windowless import PakmanWindowless

SAVE_FILE = 'qtable.dat'
GRAPHICAL_INTERFACE = True

if __name__ == '__main__':
    environment = Environment.from_str_map(maps.GAME2)
    initial_state = State.compute_state(
        environment.ghost_positions, 
        environment.initial_pakman_position,
        environment.gums,
        environment.walls
    )
    agent = QtablePakman(environment.initial_pakman_position, initial_state, environment)
    if os.path.exists(SAVE_FILE):
        agent.load(SAVE_FILE)
    
    if GRAPHICAL_INTERFACE:
        pakman = PakmanWindow(environment, agent)
        pakman.setup()
        arcade.run()
    else:
        pakman = PakmanWindowless(environment, agent)
        for i in range(1, 1000000):
            pakman.update()

    agent.save(SAVE_FILE)
    print('Qtable saved')
    plt.plot(agent.history)
    plt.show()
