import glm
from OpenGL.GL import *
from OpenGL.GLUT import *


class Ship:
    def __init__(self, position=glm.vec2(0, 0), size=glm.vec2(1, 1)):
        self.Position = position
        self.Size = size
        self.Velocity = glm.vec2(0.0, 0.0)
        self.Color = glm.vec3(1.0, 1.0, 1.0)
        self.Rotation = 0.0
        self.Sprite = None
        self.Health = 0

    def Draw(self, Renderer):
        Renderer.DrawSprite(self.Sprite, self.Position, self.Size, self.Rotation, self.Color)

    def Move(self, dt):
        self.Position = self.Position + (self.Velocity * dt)

        return self.Position


class Player(Ship):
    def __init__(self):
        super().__init__()
        self.ProjectileList = []
        self.RoF = 0.4
        self.Timer = 0

    def MakeProjectile(self, texture, dt):
        # print(self.Timer)
        if self.Timer >= self.RoF:
            self.Timer = 0
            newProjectile = Projectile()
            newProjectile.Position = glm.vec2(self.Position.x + self.Size.x / 2, self.Position.y + self.Size.y / 2)
            newProjectile.Size = glm.vec2(10, 50)
            newProjectile.Velocity = glm.vec2(0.0, -600.0)
            newProjectile.Rotation = 0.0
            newProjectile.Color = glm.vec3(1.3, 0.3, 0.1)
            newProjectile.Sprite = texture
            self.ProjectileList.append(newProjectile)


    def DrawProjectiles(self, renderer):
        for P in self.ProjectileList:
            P.Draw(renderer)

    def UpdateProjectile(self, dt):
        for P in self.ProjectileList:
            P.Position = P.Position + (P.Velocity * dt)

    def DestroyProjectile(self, projectile):
        del self.ProjectileList[projectile]


class Projectile(Ship):
    def __init__(self):
        super().__init__()

    def Draw(self, Renderer):
        Renderer.DrawSprite(self.Sprite, self.Position, self.Size, self.Rotation, self.Color)
