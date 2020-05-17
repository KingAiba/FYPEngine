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


class Player(GameObject):

    def __init__(self):
        super().__init__()
        self.ObjectType = "DYNAMIC"

    def ProccessInput(self, dt, system, ball):
        Velocity = self.Velocity * dt
        # print("DT : " + str(dt))
        # print("Velocity : " + str(Velocity))
        keys = system.GetInput()
        if keys[system.getKey("A")]:
            if self.position.x >= 0:
                self.position.x = self.position.x - Velocity.x
                if ball.Stuck:
                    ball.position.x = ball.position.x - Velocity.x

        if keys[system.getKey("D")]:
            if self.position.x <= (system.windowWidth - self.Size.x):
                self.position.x = self.position.x + Velocity.x
                if ball.Stuck:
                    ball.position.x = ball.position.x + Velocity.x

        if keys[system.getKey("SPACE")]:
            ball.Stuck = False


class BallObject(Sprite):

    def __init__(self):
        super().__init__()
        # ball attributes
        self.ObjectType = "DYNAMIC"
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
