from position import Position
from qtable_pacman import QtablePacman
from config import GAME1, GAME1_NO_GHOSTS
from game import Game
from pacman import Pacman
from state import State
from world import World


SAVE_FILE = "qtable.dat"

def pFactory(config, world: World) -> Pacman:
  position = position=Position(config["pacman"]["position"][0], config["pacman"]["position"][1])
  ghosts = []
  if config.get("blinky") and config.get("pinky") and config.get("inky") and config.get("clyde"):
    ghosts = [
      Position(config["blinky"]["position"][0], config["blinky"]["position"][1]),
      Position(config["pinky"]["position"][0], config["pinky"]["position"][1]),
      Position(config["inky"]["position"][0], config["inky"]["position"][1]),
      Position(config["clyde"]["position"][0], config["clyde"]["position"][1])
    ]
  state = State.compute_state(
    pacman_position=position,
    ghost_positions=ghosts,
    gum_positions=world.gums,
    wall_positions=world.gums
  )

  return QtablePacman(
    position=position,
    state=state
  )

  
if __name__ == '__main__':
  game = Game(GAME1_NO_GHOSTS, pacmanFactory=pFactory)

  print("training without ghosts")
  while game.rounds < 20:
    game.move()

    if game.moves >= 500 or game.isGameOver:
      print(f"round n° {game.rounds} is over")
      game.setNextRound()

  game = Game(GAME1, pacmanFactory=pFactory)

  print("training with ghosts")
  while game.rounds < 20:
    game.move()

    if game.moves >= 500 or game.isGameOver:
      print(f"round n° {game.rounds} is over")
      game.setNextRound()

  game.pacman.save()