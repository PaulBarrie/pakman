from copy import deepcopy
from enum import Enum
from random import random, sample

import numpy as np
from tqdm import tqdm
import time
import logging
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Activation, Flatten
from keras.callbacks import TensorBoard
from keras.optimizers import Adam
from collections import deque
import numpy
import tensorflow as tf

from sklearn.preprocessing import LabelEncoder

from agents.type import TargetType
from core_game.actions import Action
from core_game.pakman import Pakman
from core_game.position import Position
from environment.environment import Environment
from agents.qtable_pakman import QtablePakman
from environment.state import State, DQLearnState

REPLAY_MEMORY_SIZE = 50_000
MIN_REPLAY_MEMORY_SIZE = 1_000
UPDATE_WEIGHTS_EVERY = 5
MODEL_NAME = "256x2"
EPISODES = 20_000

"""
https://towardsdatascience.com/deep-q-learning-tutorial-mindqn-2a4c855abffc
https://pythonprogramming.net/training-deep-q-learning-dqn-reinforcement-learning-python-tutorial/?completed=/deep-q-learning-dqn-reinforcement-learning-python-tutorial/
"""


# Own Tensorboard class
class ModifiedTensorBoard(TensorBoard):

    # Overriding init to set initial step and writer (we want one log file for all .fit() calls)
    def __init__(self, **kwargs):
        self.step = 1

    # Overriding this method to stop creating default log writer
    def set_model(self, model):
        pass

    # Override, saves logs with our step number
    # (otherwise every .fit() will start writing from 0th step)
    def on_epoch_end(self, epoch, logs=None):
        self.update_stats(**logs)

    # Override
    # We train for one batch only, no need to save anything at epoch end
    def on_batch_end(self, batch, logs=None):
        pass

    # Override, so won't close writer
    def on_train_end(self, _):
        pass

    # Custom method for saving own metrics
    # Creates writer, writes custom metrics and closes writer
    def update_stats(self, **stats):
        self._write_logs(stats, self.step)


class DQLearnPakman(Pakman):
    """
        environment: Environment -> Environment of the fame
        initial_step: int -> Initial step of the game
        binary_input: bool -> If the input is binary or not
        output_dimension: int -> Dimension of the output (# of actions)
        batch_size: int -> Size of the batch to train the model
        dropout_neuron_rate: float -> Rate of the dropout neuron
        learning_rate: float -> Learning rate of the model
        min_replay_size: int -> Minimum required size to train the model
    """

    def __init__(self, initial_position: Position, initial_state: DQLearnState, env: Environment, qtable=None,
                 history=None, alpha=1, gamma=0.9, cooling_rate=0.999, multinomial_input=False,
                 target_type=TargetType.REWARD, output_dimension=4, batch_size=1, dropout_neuron_rate=0.2,
                 learning_rate=1, min_replay_size=MIN_REPLAY_MEMORY_SIZE):
        super().__init__(initial_position)

        self.__history = history
        self.__alpha = alpha
        self.__gamma = gamma
        self.__cooling_rate = cooling_rate
        self.__multinomial_input = multinomial_input
        self.__target_type = target_type
        self.__output_dimension = output_dimension
        self.__batch_size = batch_size
        self.__dropout_neuron_rate = dropout_neuron_rate
        self.__learning_rate = learning_rate
        self.__min_replay_size = min_replay_size

        self.__qtable_pakman = QtablePakman(initial_position, initial_state, env, qtable, history, alpha, gamma,
                                            cooling_rate)

        self.__input_shape = (self.__qtable_pakman.environment.width, self.__qtable_pakman.environment.height, 1)
        if output_dimension is None:
            output_dimension = len(Action.as_list())

        self.__multinomial_input = multinomial_input
        self.__target_type = target_type
        self.__output_dimension = output_dimension
        self.__batch_size = batch_size
        self.__learning_rate = learning_rate
        self.__min_replay_size = min_replay_size
        self.__dropout_neuron_rate = dropout_neuron_rate
        self.__model = self.build_model()
        self.__data = {
            "X": [],
            "Y": []
        }
        # Target model this is what we .predict against every step
        self.replay_memory = deque(maxlen=min_replay_size)
        self.tensorboard = ModifiedTensorBoard(log_dir=f"logs/{MODEL_NAME}-{int(time.time())}")
        self.target_update_counter = 0

    def create_model(self, kernels=None, activation="relu") -> Sequential:
        if kernels is None:
            kernels = [(3, 3), (3, 3), (3, 3)]
        model = Sequential()
        apply_layer = lambda kernel_size: map(lambda x: model.add(x), [
            Conv2D(self.__batch_size, kernel_size, input_shape=self.__input_shape),
            Activation(activation),
            Dropout(self.__dropout_neuron_rate),
        ])
        for kernel in kernels:
            apply_layer(kernel)

        model.add(Dense(self.__output_dimension, activation="linear"))

        return model

    def compile_model(self, model: Sequential, loss="mse", metrics=None) -> Sequential:
        if metrics is None:
            metrics = ["accuracy"]
        optimizer = tf.keras.optimizers.SGD(learning_rate=self.__learning_rate)
        model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
        return model

    def build_model(self) -> Sequential:
        model = self.create_model()
        model = self.compile_model(model)
        # model.build(self.)
        # model.set_weights(self.__model.get_weights())
        return model

    def update_replay_memory(self, transition):
        self.replay_memory.append(transition)

    def get_multinomial_inputs(self) -> numpy.ndarray:
        label_encoder = LabelEncoder()
        state_array = numpy.array(self.__qtable_pakman.environment.as_multinomial_array())

        for i in range(state_array.shape[0]):
            state_array[i] = label_encoder.fit_transform(state_array[i])

        return state_array

    def predicted_best_action(self, X: numpy.array) -> Action:
        rewards = self.__model.predict(X)
        return Action.as_list()[numpy.argmax(rewards)]

    def fit_model(self,
                  XY_train: tuple[numpy.array, numpy.array],
                  XY_test: tuple[numpy.array, numpy.array], terminal_state):
        X_train, Y_train = XY_train
        X_test, Y_test = XY_test
        self.__model.fit(
            x=X_train,
            y=Y_train,
            batch_size=self.__batch_size,
            verbose=0,
            shuffle=False,
            validation_data=(X_test, Y_test),
            callbacks=[self.tensorboard] if terminal_state else None
        )
        print(self.__model.summary())

    def get_reward_outputs(self):
        y_rewards = []
        for action in Action.as_list():
            position, state, reward, isDead = self.__qtable_pakman.environment.do_dry(action,
                                                                                      self.__qtable_pakman.position)
            y_rewards.append(reward)
        return numpy.array(y_rewards).reshape(self.__output_dimension, 1)

    def get_qtable_outputs(self):
        y_rewards = []
        for action in Action.as_list():
            position, state, reward, isDead = self.__qtable_pakman.environment.do_dry(action,
                                                                                      self.__qtable_pakman.position)
            qtable = self.__qtable_pakman.update_q_table(state, action, reward)
            y_rewards.append(qtable[state][action])
        return numpy.array(y_rewards, shape=(self.__output_dimension, 1))

    def get_outputs(self):
        if self.__target_type == TargetType.REWARD:
            return self.get_reward_outputs()
        elif self.__target_type == TargetType.QTABLE:
            return self.get_qtable_outputs()


    def get_inputs(self) -> numpy.ndarray:
        if self.__multinomial_input:
            return self.__qtable_pakman.environment.data_environment
        else:
            return self.get_multinomial_inputs()

    def train(self):
        XBatches = np.split(np.array(self.__data["X"]), int(len(self.__data["X"]) * self.__batch_size))
        YBatches = np.split(np.array(self.__data["Y"]), int(len(self.__data["Y"]) * self.__batch_size))
        terminal_state = True
        for XBatch, YBatch in zip(XBatches, YBatches):
            self.fit_model(XBatch, YBatch, terminal_state)
            if terminal_state:
                self.target_update_counter += self.__batch_size

            if self.target_update_counter > UPDATE_WEIGHTS_EVERY:
                self.__model.set_weights(self.__model.get_weights())
                self.target_update_counter = 0

    def step(self, action=None) -> tuple[Action, float]:
        # Get a minibatch of random samples from memory replay table
        # minibatch = random.sample(self., self.__batch_size)

        # Get current states from minibatch, then query NN model for Q values
        action = self.__qtable_pakman._best_action()
        X = self.get_inputs()
        Y = self.get_outputs()
        self.__data["X"].append(X)
        self.__data["Y"].append(Y)
        print("TRAIN")
        print(len(self.__data["X"]), self.__min_replay_size)
        print(len(self.__data["Y"]), self.__min_replay_size)

        if len(self.__data["X"]) < self.__min_replay_size and len(self.__data["Y"]) < self.__min_replay_size:
            # Chose best action and do nothing
            print("Chose best action and do nothing")
            return self.__qtable_pakman.step(action)
        if numpy.random.rand() < self.__learning_rate:
            # We train the model and choose best action
            print("Training model")
            self.train()
        else:
            # Then we predict the future reward and action
            print("Predicting future reward")
            action = self.predicted_best_action(X)

        return self.__qtable_pakman.step(action)

    def reset(self, initial_position: Position, initial_state: State, environment: Environment, qtable=None,
              history=None):
        qtable_pakman = deepcopy(
            self.__qtable_pakman.reset(initial_position, initial_state, environment, qtable, history))
        return DQLearnPakman(initial_position, initial_state, environment,
                             self.__history, alpha=1, gamma=0.9, cooling_rate=0.999, multinomial_input=False,
                             target_type=TargetType.REWARD, output_dimension=None, batch_size=1,
                             dropout_neuron_rate=0.2,
                             learning_rate=1, min_replay_size=MIN_REPLAY_MEMORY_SIZE)

    def get(self):
        return self

    def save(self, qtable_file="qtable_pakman.dump", model_file="model_pakman.h5") -> None:
        self.__qtable_pakman.save(qtable_file)
        self.__model.save(model_file)

    def load(self, qtable_file="qtable_pakman.dump", model_file="model_pakman.h5") -> None:
        self.__qtable_pakman.load(qtable_file)
        self.__model = tf.keras.models.load_model(model_file)

    @property
    def score(self) -> float:
        if self.__qtable_pakman is not None:
            return self.__qtable_pakman.score
        return self.__qtable_pakman.score

    @property
    def temperature(self) -> float:
        return self.__qtable_pakman.temperature

    @property
    def qtable(self):
        return self.__qtable_pakman.qtable

    @property
    def history(self):
        return self.__qtable_pakman.history
