import os
from actions import Action
from position import Position
from qtable_pacman import QtablePacman
from config import GAME1, GAME1_NO_GHOSTS, GAME2, GAME2_NO_GHOSTS, GAME3
from game import Game
from pacman import Pacman
from state import State, compute_state
from world import World


SAVE_FILE = "qtable.dat"

def pFactory(config, world: World, qtable = None, history = None) -> Pacman:
  position = position=Position(config["pacman"]["position"][0], config["pacman"]["position"][1])
  ghosts = []
  if config.get("blinky"):
    print("Blinky config")
    ghosts.append(Position(config["blinky"]["position"][0], config["blinky"]["position"][1]))
  if config.get("pinky") :
    print("Pinky config")
    ghosts.append(Position(config["pinky"]["position"][0], config["pinky"]["position"][1]))
  if config.get("inky"):
    print("Inky config")
    ghosts.append(Position(config["inky"]["position"][0], config["inky"]["position"][1])) 
  if config.get("clyde"):
    print("Clyde config")
    ghosts.append(Position(config["clyde"]["position"][0], config["clyde"]["position"][1]))

  state = compute_state(
    pacman_position=position,
    ghost_positions=ghosts,
    gum_positions=world.getGums(),
    wall_positions=world.walls
  )

  return QtablePacman(
    position=position,
    state=state,
    qtable=qtable,
    history=history
  )

  
def train():
  game = Game(GAME2_NO_GHOSTS, pacmanFactory=pFactory)
  game.pacman.heat()
  
  if os.path.exists(SAVE_FILE):
    game.pacman.load(SAVE_FILE)
  
  print("training without ghosts")
  while game.rounds < 200:
    game.move()

    if game.moves >= 10000 or game.isGameOver:
      print(f"round {game.rounds}")
      game.setNextRound()
      game.pacman.heat()
  game.pacman.save(SAVE_FILE)

  game = Game(GAME2, pacmanFactory=pFactory)
  game.pacman.load(SAVE_FILE)
  game.pacman.heat()

  if len(game.ghosts):
    print("training with ghosts")
    while game.rounds < 200:
      game.move()

      if game.moves >= 10000 or game.isGameOver:
        print(f"round {game.rounds}")
        game.setNextRound()
        game.pacman.heat()
    game.pacman.save(SAVE_FILE)