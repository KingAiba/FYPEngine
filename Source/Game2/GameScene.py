import random
import glm
from GameObjects import Ship
from GameObjects import Player
from Renderer.ResourseManager import Resources


class Scene:
    def __init__(self, background, ships, bosses, width, height):
        self.background = background
        self.ShipAmount = ships
        self.BossAmount = bosses
        self.SceneWidth = width
        self.SceneHeight = height
        self.Curr = []
        self.SpawnTimer = 0

    def UpdateScene(self, amount, dt):
        self.RemoveDead()

        for ship in self.Curr:
            ship.Position = ship.Position + (ship.Velocity * dt)

        if self.SpawnTimer >= 2:
            for x in range(0, amount):
                if self.ShipAmount > 0:
                    randPos = glm.vec2(random.uniform(150, self.SceneWidth - 150), 0.0)
                    size = glm.vec2(100, 100)
                    velocity = glm.vec2(0, 100)
                    NewShip = Ship(randPos, size)
                    NewShip.Velocity = velocity
                    NewShip.Health = 3
                    NewShip.Sprite = Resources.Textures["RedShip"]

                    self.Curr.append(NewShip)
                self.ShipAmount = self.ShipAmount - 1
            self.SpawnTimer = 0
        self.SpawnTimer = self.SpawnTimer + dt

    def DrawShips(self, renderer):
        for ship in self.Curr:
            ship.Draw(renderer)

    def StartScene(self, renderer, backgroundColor):
        renderer.DrawSprite(self.background, glm.vec2(0, 0), glm.vec2(self.SceneWidth, self.SceneHeight),
                            0.0, backgroundColor)

    def RemoveDead(self):
        Ind = 0
        for ship in self.Curr:
            if ship.Health <= 0:
                del self.Curr[Ind]
            Ind = Ind + 1

    def DelShip(self, Ind):
        del self.Curr[Ind]
