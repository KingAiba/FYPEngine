
import os
import sys

sys.path.append(os.path.dirname(__file__) + "/../")

from Source.System.System import System
from Game.GameLevel import GameLevel


def main():
    GameSystem = System()
    GameSystem.InitSystem()

    Level = GameLevel(GameSystem)
    Level.InitLevel()
    GameSystem.LevelManager = Level

    GameSystem.GameLoop(0)

    GameSystem.SystemTerminate()
    return 0


main()
