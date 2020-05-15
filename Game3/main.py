import os
import sys

# sys.path.append(os.path.dirname(__file__) + "/../")
sys.path.append(sys.path[0] + "/../")
from Source.System.System import System
from Game3.GameLevel import GameLevel


def main():
    GameSystem = System()
    GameSystem.InitSystem()

    Level1 = GameLevel(GameSystem)
    Level1.InitLevel()
    GameSystem.LevelManager = Level1

    GameSystem.GameLoop(1)

    GameSystem.SystemTerminate()
    return 0


main()
