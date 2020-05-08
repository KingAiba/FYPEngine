import os
import sys
import glm
from System.System import System
from System.LevelManager import LevelManager
from System.gameObject import Sprite
from Source.System.animationComponent import Animation

cameraVelocity = float(250)
Anim1 = Animation()
Anim1.speed = 0.30
Anim1.AnimationList = [glm.vec2(1, 1), glm.vec2(2, 1), glm.vec2(3, 1), glm.vec2(4, 1)]

Anim2 = Animation()
Anim2.speed = 0.25
Anim2.AnimationList = [glm.vec2(1, 2), glm.vec2(2, 2), glm.vec2(3, 2), glm.vec2(4, 2), glm.vec2(5, 2), glm.vec2(6, 2)]


class Level1(LevelManager):

    def __init__(self, system):
        super().__init__(system)
        self.player = None

    def InitLevel(self):
        super().InitLevel()

        # player = Sprite(os.path.dirname(__file__) + "/../res/GameObjects/Player.xml")
        Obj1 = Sprite(os.path.abspath(__file__) +"/../../res/GameObjects/Object1.xml")
        #
        Obj1.Animated = True
        Obj1.addAnimation(Anim1)
        Obj1.addAnimation(Anim2)
        Obj1.TexID = 1
        Obj1.VerticalFlip = 0
        self.player = Obj1

        # self.AddObject(player)
        self.AddObject(Obj1)

        self.System.setCamera(0.0, 800, 600, 0.0)

    def Update(self, dt):

        pos = self.System.Camera.getPosition()
        # print(self.System.GetDeltaTime())
        keys = self.System.GetInput()

        if keys[self.System.getKey("W")]:
            pos.y = pos.y - cameraVelocity * (dt)

        if keys[self.System.getKey("A")]:
            pos.x = pos.x - cameraVelocity * (dt)
            self.player.VerticalFlip = 1

        if keys[self.System.getKey("S")]:
            pos.y = pos.y + cameraVelocity * (dt)

        if keys[self.System.getKey("D")]:
            pos.x = pos.x + cameraVelocity * (dt)
            self.player.VerticalFlip = 0

        if keys[self.System.getKey("SPACE")]:
            self.player.ChangeAnimationState(1)
        else:
            self.player.ChangeAnimationState(0)

        self.System.UpdateCamera(pos.x, pos.y, 0.0, 1)
        super().Update(dt)


# class Level2(LevelManager):
#
#     def InitLevel(self):
#         super().InitLevel()
#
#         player = Sprite(os.path.dirname(__file__) + "/../res/GameObjects/Player.xml")
#
#         self.AddObject(player)
#
#         self.System.setCamera(0.0, 500, 500, 0.0)
#
#     def Update(self, dt):
#
#         pos = self.System.Camera.getPosition()
#         # print(self.System.GetDeltaTime())
#         keys = self.System.GetInput()
#
#         if keys[self.System.getKey("W")]:
#             pos.y = pos.y - cameraVelocity * (dt)
#
#         if keys[self.System.getKey("A")]:
#             pos.x = pos.x - cameraVelocity * (dt)
#
#         if keys[self.System.getKey("S")]:
#             pos.y = pos.y + cameraVelocity * (dt)
#
#         if keys[self.System.getKey("D")]:
#             pos.x = pos.x + cameraVelocity * (dt)
#
#         self.System.UpdateCamera(pos.x, pos.y, 0.0, 0)
#         super(Level2, self).Update(dt)


newSystem = System()
newSystem.InitSystem()
Level1 = Level1(newSystem)
newSystem.LevelManager = Level1
Level1.InitLevel()
newSystem.GameLoop(1)
