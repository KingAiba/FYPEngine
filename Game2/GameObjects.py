import glm
import os
import sys

sys.path.append(os.path.dirname(__file__) + "/../")

from Source.System.gameObject import Sprite


class Ship(Sprite):
    def __init__(self):
        super().__init__()

        self.Color = glm.vec3(1.0, 1.0, 1.0)
        self.Sprite = None
        self.Health = 0


class Player(Ship):
    def __init__(self):
        super().__init__()
        self.ProjectileList = []
        self.RoF = 0.33
        self.Timer = 0

    def MakeProjectile(self, texture, dt):
        # print(self.Timer)
        if self.Timer >= self.RoF:
            self.Timer = 0
            newProjectile = Projectile()
            newProjectile.position = glm.vec2(self.position.x + self.Size.x / 2, self.position.y + self.Size.y / 2)
            newProjectile.Size = glm.vec2(10, 50)
            newProjectile.Velocity = glm.vec2(0.0, -600.0)
            newProjectile.Rotation = 0.0
            newProjectile.Color = glm.vec3(1.3, 0.3, 0.1)
            newProjectile.Texture = texture
            self.ProjectileList.append(newProjectile)

    def DrawProjectiles(self, system):
        for P in self.ProjectileList:
            P.Draw(system)

    def UpdateProjectile(self, dt):
        for P in self.ProjectileList:
            P.position = P.position + (P.Velocity * dt)

    def DestroyProjectile(self, projectile):
        del self.ProjectileList[projectile]


class Projectile(Sprite):
    def __init__(self):
        super().__init__()

