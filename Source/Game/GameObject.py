import glm
from OpenGL.GL import *
from OpenGL.GLUT import *
from Source.Renderer.SpriteRender import SpriteRender
from Source.Renderer.texture import Texture


class GameObject:

    def __init__(self):
        self.Position = glm.vec2(0, 0)
        self.Size = glm.vec2(1, 1)
        self.Velocity = glm.vec2(0.0, 0.0)
        self.Color = glm.vec3(1.0, 1.0, 1.0)
        self.Rotation = 0.0  # float
        # texture obj
        self.Sprite = None
        # flags
        self.IsSolid = GL_FALSE
        self.Destroyed = GL_FALSE

    def Draw(self, Renderer):
        Renderer.DrawSprite(self.Sprite, self.Position, self.Size, self.Rotation, self.Color)


class BallObject(GameObject):

    def __init__(self):
        super().__init__()
        # ball attributes
        self.Radius = float(0)
        self.Stuck = GL_TRUE

    def Move(self, dt, window_width):
        if not self.Stuck:
            self.Position = self.Position + (self.Velocity * dt)

            if self.Position.x <= 0.0:
                self.Velocity.x = -self.Velocity.x
                self.Position.x = 0.0

            elif (self.Position.x + self.Size.x) >= window_width:
                self.Velocity.x = -self.Velocity.x
                self.Position.x = window_width - self.Size.x

            if self.Position.y <= 0.0:
                self.Velocity.y = -self.Velocity.y
                self.Position.y = 0.0

        return self.Position

    def Reset(self, position, velocity):
        self.Position = position
        self.Velocity = velocity
        self.Stuck = GL_TRUE


class Particle:
    def __init__(self):
        
        self.Life = float(0.0)
