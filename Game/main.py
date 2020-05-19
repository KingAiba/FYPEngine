
import os
import sys

# sys.path.append(os.path.dirname(__file__) + "/../")
sys.path.append(sys.path[0] + "/../")
from Source.System.System import System
from Game.GameLevel import GameLevel
from Game.GameLevel import Menu


def main():
    GameSystem = System()
    GameSystem.InitSystem()

    menu = Menu(GameSystem)
    menu.InitLevel()
    GameSystem.LevelManager = menu

    GameSystem.GameLoop(0)

    GameSystem.SystemTerminate()
    return 0


main()
