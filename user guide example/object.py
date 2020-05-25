import os
import sys

# sys.path.append(os.path.dirname(__file__) + "/../")
from Source.System.gameObject import Sprite
from Source.Utility.glmVec import GetVec2


class Player(Sprite):
    def __init__(self, filepath=None):
        super().__init__(filepath)
        self.Velocity = GetVec2(200, 200)
        self.ObjectType = "DYNAMIC"

    def ProccessInput(self, dt, system):
        keys = system.GetInput()

        if keys[system.getKey("S")]:
            if self.position.y <= (system.windowHeight - self.Size.y):
                self.MoveY(dt, self.Velocity.y)

        if keys[system.getKey("W")]:
            if self.position.y >= 0:
                self.MoveY(dt, -self.Velocity.y)

        if keys[system.getKey("A")]:
            if self.position.x >= 0:
                self.MoveX(dt, -self.Velocity.x)

        if keys[system.getKey("D")]:
            if self.position.x <= (system.windowWidth - self.Size.x):
                self.MoveX(dt, self.Velocity.x)


class Block(Sprite):
    def __init__(self, filepath=None):
        super().__init__(filepath)
