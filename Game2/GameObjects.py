import os
import sys


# sys.path.append(os.path.dirname(__file__) + "/../")
sys.path.append(sys.path[0] + "/../")

from Source.System.gameObject import Sprite
from Source.Utility.glmVec import GetVec2, GetVec3
from Source.System.audioManager import AudioManager


class Ship(Sprite):
    def __init__(self):
        super().__init__()

        self.Color = GetVec3(1.0, 1.0, 1.0)
        self.Sprite = None
        self.Health = 0
        self.ObjectType = "DYNAMIC"


class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.Health = 0
        self.ProjectileList = []
        self.RoF = 0.33
        self.Timer = 0
        self.ObjectType = "DYNAMIC"

    def MakeProjectile(self, texture, dt, audio):
        # print(self.Timer)
        if self.Timer >= self.RoF:
            self.Timer = 0
            newProjectile = Projectile()
            newProjectile.position = GetVec2(self.position.x + self.Size.x / 2, self.position.y + self.Size.y / 2)
            newProjectile.Size = GetVec2(10, 50)
            newProjectile.Velocity = GetVec2(0.0, -600.0)
            newProjectile.Rotation = 0.0
            newProjectile.Color = GetVec3(1.3, 0.3, 0.1)
            newProjectile.Texture = texture
            self.ProjectileList.append(newProjectile)
            audio.Play("wep1")


    def Update(self, dt, system, audio):
        self.ProccessInput(dt, system, audio)
        self.UpdateProjectile(dt)

    def Draw(self, system):
        super().Draw(system)
        self.DrawProjectiles(system)

    def ProccessInput(self, dt, system, audio):
        keys = system.GetInput()

        self.Timer = self.Timer + dt
        Velocity = self.Velocity * dt

        if keys[system.getKey("S")]:
            if self.position.y <= (system.windowHeight - self.Size.y):
                self.position.y = self.position.y + Velocity

        if keys[system.getKey("W")]:
            if self.position.y >= 0:
                self.position.y = self.position.y - Velocity

        if keys[system.getKey("A")]:
            if self.position.x >= 0:
                self.position.x = self.position.x - Velocity

        if keys[system.getKey("D")]:
            if self.position.x <= (system.windowWidth - self.Size.x):
                self.position.x = self.position.x + Velocity

        if keys[system.getKey("SPACE")]:
            self.MakeProjectile("ball", dt, audio)

    def DrawProjectiles(self, system):
        for P in self.ProjectileList:
            P.Draw(system)

    def UpdateProjectile(self, dt):
        for P in self.ProjectileList:
            P.position = P.position + (P.Velocity * dt)

    def DestroyProjectile(self, projectile):
        del self.ProjectileList[projectile]


# 12 - 8

class Projectile(Sprite):
    def __init__(self):
        super().__init__()
        self.ObjectType = "DYNAMIC"
