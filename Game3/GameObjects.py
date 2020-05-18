import os
import sys

# sys.path.append(os.path.dirname(__file__) + "/../")
sys.path.append(sys.path[0] + "/../")
from Source.System.gameObject import Sprite


class Player(Sprite):
    def __init__(self, FilePath=None):
        super().__init__(FilePath)
        self.CollisionFlag = 0
        self.acceleration = 500
        self.JumpFlag = 0
        self.ObjectType = "DYNAMIC"

    def jump(self):
        if self.CollisionFlag == 1 and self.JumpFlag == 0:
            self.position.y -= 10
            self.acceleration = -250
            self.JumpFlag = 1

    def gravity(self, dt):
        if self.acceleration < 500:
            self.acceleration += 500 * dt

        if self.CollisionFlag == 0:

            self.Velocity.y += self.acceleration * dt
        else:
            self.Velocity.y = 0

    def Update(self, dt):
        self.gravity(dt)
        self.Move(dt)
        super().Update(dt)

    def TileCollision(self, tile):
        ColX = False
        ColY = False
        Col = False

        if ((self.position.x + self.Size.x) >= tile.position.x) and (
                (tile.position.x + tile.Size.x) >= self.position.x):
            ColX = True
        if ((self.position.y + self.Size.y) >= tile.position.y) and (
                (tile.position.y + tile.Size.y) >= self.position.y):
            ColY = True

        if ColX and ColY and ((self.position.y + self.Size.y / 2) < tile.position.y):
            Col = True

        return Col


class Tile(Sprite):
    def __init__(self, FilePath=None):
        super().__init__(FilePath)


class Object(Sprite):
    def __init__(self, FilePath=None):
        super().__init__(FilePath)
