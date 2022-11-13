import sys

from gui_pacman import launchGUI
from train import train


GUI_ARG = "--gui"
TRAIN_ARG = "--train"
VALID_ARGS = [GUI_ARG, TRAIN_ARG]

if __name__ == "__main__":
  arg = GUI_ARG

  if len(sys.argv) == 2:
    arg = sys.argv[1]
    if arg not in VALID_ARGS:
      raise Exception("Invalid CLI argument, expected '--gui' or '--train'")

  if arg == GUI_ARG:
    launchGUI()
  else:
    train()

    