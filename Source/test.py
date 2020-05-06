import os
import sys
from System.System import System
from System.LevelManager import LevelManager
from System.gameObject import Sprite



class LevelTest(LevelManager):

    def InitLevel(self):
        super().InitLevel()

        player = Sprite(os.path.dirname(__file__) + "/../res/GameObjects/Player.xml")
        Obj1 = Sprite(os.path.dirname(__file__) + "/../res/GameObjects/Object1.xml")
        self.AddObject(player)
        self.AddObject(Obj1)



newSystem = System()
Level1 = LevelTest(newSystem)
newSystem.LevelManager = Level1
Level1.InitLevel()
newSystem.GameLoop()




