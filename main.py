import os
import random
import numpy as np
import tensorflow as tf

from agents.dqlearn_pakman import DQLearnPakman, TargetType
from agents.qtable_pakman import QtablePakman
from environment.state import State
from pakman_window import PakmanWindow
from environment.environment import Environment
import maps
import arcade
import matplotlib.pyplot as plt
import logging

from pakman_windowless import PakmanWindowless

FOLDER_SEPARATING_CHAR = '/'
QTABLE_FILE = 'qtable.dat'
MODEL_FILE = 'model.h5'
MIN_REPLAY_MEMORY_SIZE = 1_000

GRAPHICAL_INTERFACE = True

random.seed(1)
np.random.seed(1)


def create_dirs():
    qtable_split = QTABLE_FILE.split(FOLDER_SEPARATING_CHAR)
    qtable_folder = '.'
    if len(qtable_split) > 1:
        qtable_folder = FOLDER_SEPARATING_CHAR.join(qtable_split[0:-1])
    if not os.path.exists(qtable_folder):
        logging.error(qtable_folder)
        os.makedirs(qtable_folder)

    model_folder_split = MODEL_FILE.split()
    model_folder = '.'
    if len(qtable_split) > 1:
        model_folder = FOLDER_SEPARATING_CHAR.join(model_folder_split[0:-1])
    if not os.path.exists(model_folder):
        os.makedirs(model_folder)
    if not os.path.exists(model_folder):
        os.mkdir(model_folder)


if __name__ == '__main__':
    environment = Environment.from_str_map(maps.GAME2)
    initial_state = State.compute_state(
        environment.ghost_positions,
        environment.initial_pakman_position,
        environment.gums,
        environment.walls
    )
    create_dirs()
    # agent = QtablePakman(environment.initial_pakman_position, initial_state, environment)

    agent = DQLearnPakman(
        initial_position=environment.initial_pakman_position,
        initial_state=initial_state,
        env=environment,
        multinomial_input=False,
        target_type=TargetType.REWARD,
        output_dimension=4, batch_size=100, dropout_neuron_rate=0.2, learning_rate=0.8,
        min_replay_size=MIN_REPLAY_MEMORY_SIZE)
    # gets trained every step
    if os.path.exists(QTABLE_FILE) and os.path.exists(MODEL_FILE):
        agent.load(QTABLE_FILE, MODEL_FILE)

    if GRAPHICAL_INTERFACE:
        pakman = PakmanWindow(environment, agent)
        pakman.setup()
        arcade.run()
    else:
        pakman = PakmanWindowless(environment, agent)
        for i in range(1, 50000):
            pakman.update()

    agent.save(qtable_file=QTABLE_FILE, model_file=MODEL_FILE)

    print('Qtable and model saved')
    plt.plot(agent.history)
    plt.show()
