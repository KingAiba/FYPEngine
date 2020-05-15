import glm
import os
import sys

# sys.path.append(os.path.dirname(__file__) + "/../")
sys.path.append(sys.path[0] + "/../")

from OpenGL.GL import *
from OpenGL.GLUT import *
from Source.System.gameObject import *


class GameObject(Sprite):

    def __init__(self):
        super().__init__()
        # texture obj
        self.Texture = ""
        # flags
        self.IsSolid = False
        self.Destroyed = False


class BallObject(Sprite):

    def __init__(self):
        super().__init__()
        # ball attributes
        self.Radius = float(0)
        self.Stuck = True

    def BallMove(self, dt, window_width):
        if not self.Stuck:
            self.position = self.position + (self.Velocity * dt)

            if self.position.x <= 0.0:
                self.Velocity.x = -self.Velocity.x
                self.position.x = 0.0

            elif (self.position.x + self.Size.x) >= window_width:
                self.Velocity.x = -self.Velocity.x
                self.position.x = window_width - self.Size.x

            if self.position.y <= 0.0:
                self.Velocity.y = -self.Velocity.y
                self.position.y = 0.0

        return self.position

    def Reset(self, position, velocity):
        self.position = position
        self.Velocity = velocity
        self.Stuck = True


