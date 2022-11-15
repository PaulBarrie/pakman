import pickle
from random import choice, random
from actions import Action, Direction
from game import Game
from pacman import Pacman
from position import Position
from state import State


class QtablePacman(Pacman):
  @property
  def state(self):
      return self.__state

  @property
  def score(self) -> float:
      return self.__score

  @property
  def history(self) -> list[float]:
      return self.__history

  @property
  def temperature(self) -> float:
      return self.__temperature

  def __init__(self, position: Position, state: State, qtable=None, history=None, alpha=0.9, gamma=0.8, epsilon=0.20, cooling_rate=0.999) -> None:
      super().__init__(position)

      self.__temperature = 0.0
      self.__score = 0.0
      self.__state = state
      self.qtable: dict[
        State, 
        dict[Action, float]
      ] = qtable if qtable != None else {}
      self.__alpha = alpha
      self.__gamma = gamma
      self.__epsilon = epsilon
      self.__history = history if history != None else []
      self.__cooling_rate = cooling_rate

  def heat(self) -> None:
      self.__temperature = self.__epsilon

  def _best_action(self) -> Action:
    if random() < self.__temperature:
      # self.__temperature *= self.__cooling_rate
      return choice(Action.as_list())

    actions = self.__getActionsFromQtable(self.__state)
    return max(actions, key=actions.get)

  def step(self, game: Game) -> None:
    action = self._best_action()
    previousLives = self._lives

    # print(f"{self.__state} | {action}")
    state, reward, self._position = game.do(self._position, action, self.__state)
    maxQ = max(self.__getActionsFromQtable(state).values())
    delta = self.__alpha * (reward + self.__gamma * maxQ - self.__getActionsFromQtable(self.__state)[action])
    self.qtable[self.__state][action] += delta

    # direction already changed if pacman has died !
    if previousLives == self._lives:
      self._direction = action.to_direction()

    self.__state = state
    self.__score += reward   

  def refreshState(self, state: State) -> None:
    self.__state = state

  def __getActionsFromQtable(self, state: State) -> dict[Action, float]:
    if state not in self.qtable:
      default = { k: 0.0 for k in Action.as_list() }
      self.qtable[state] = default
      return default

    return self.qtable[state]

  def load(self, filename = "qtable.dat") -> None:
    with open(filename, 'rb') as file:
      self.qtable, self.__history = pickle.load(file)

  def save(self, filename = "qtable.dat") -> None:
    with open(filename, 'wb') as file:
      pickle.dump((self.qtable, self.__history), file)

  def reset(self, state: State) -> None:
    # save final round score
    self.__history.append(self.__score)

    self._lives = self._maxLives
    self._position = self._initialPosition
    self._direction = Direction.WEST
    self.__state = state
    self.__temperature = 0.0
    self.__score = 0.0
