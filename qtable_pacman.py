import pickle
from random import choice, random
from actions import Action
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

  def __init__(self, position: Position, state: State, qtable=None, history=None, alpha=1, gamma=0.8, cooling_rate=0.999) -> None:
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
      self.__history = history if history != None else []
      self.__cooling_rate = cooling_rate

  def heat(self) -> None:
      self.__temperature = 1.0

  def _best_action(self) -> Action:
    if random() < self.__temperature:
      self.__temperature *= self.__cooling_rate
      return choice(Action.as_list())

    actions = self.__qtable_get_or_create(self.__state)
    return max(actions, key=actions.get)

  def step(self, game: Game) -> None:
    action = self._best_action()
    prevLives = self._lives

    state, reward, self._position = game.do(self._position, action, self.__state)
    maxQ = max(self.__qtable_get_or_create(state).values())
    delta = self.__alpha * (reward + self.__gamma * maxQ - self.__qtable_get_or_create(self.__state)[action])
    self.qtable[self.__state][action] += delta

    if prevLives == self._lives:
      self._direction = action.to_direction()
    self.__state = state
    self.__score += reward
    self.__history.append(self.__score)

    # print(f"{state}")

  def __qtable_get_or_create(self, state: State) -> dict[Action, float]:
    return self.qtable.setdefault(
      state,
      { k: 0.0 for k in Action.as_list() }
    )

  def load(self, filename = "qtable.dat") -> None:
    with open(filename, 'rb') as file:
      self.qtable, self.__history = pickle.load(file)

  def save(self, filename = "qtable.dat") -> None:
    with open(filename, 'wb') as file:
      pickle.dump((self.qtable, self.__history), file)

  # def __repr__(self) -> str:
  #   res = f'Agent {self.__state}\n'
  #   res += str(self.qtable)
  #   return res
