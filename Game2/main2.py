
import os
import sys
sys.path.append(os.path.dirname(__file__) + "/../")
from Source.System.System import System
from Game2.GameScene import Scene



def main():
    GameSystem = System()
    GameSystem.InitSystem()

    Level = Scene(15, 15, GameSystem.windowWidth, GameSystem.windowHeight,GameSystem)
    Level.InitScene()
    GameSystem.LevelManager = Level

    GameSystem.GameLoop(0)

    GameSystem.SystemTerminate()
    return 0


main()
