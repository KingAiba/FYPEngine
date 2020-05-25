import os
import sys

# sys.path.append(os.path.dirname(__file__) + "/../")
from Source.System.System import System
from level import GameLevel


def main():
    GameSystem = System()
    GameSystem.InitSystem()

    lvl = GameLevel(GameSystem)
    lvl.InitLevel()
    GameSystem.LevelManager = lvl

    GameSystem.GameLoop(0)

    GameSystem.SystemTerminate()
    return 0


main()
