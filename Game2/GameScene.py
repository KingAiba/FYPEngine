import random
import glm
import sys
import os
#sys.path.append(os.path.dirname(__file__) + "/../")
sys.path.append(sys.path[0] + "/../")
from Game2.GameObjects import Ship
from Game2.GameObjects import Player
from Source.System.LevelManager import LevelManager

Player_Velocity = float(550.0)
Player_Size = glm.vec2(125, 125)


class Scene(LevelManager):
    def __init__(self, ships, bosses, width, height, system):
        super().__init__(system)
        self.player = None
        self.background = ""
        self.ShipAmount = ships
        self.BossAmount = bosses
        self.SceneWidth = width
        self.SceneHeight = height
        self.gameObjects = []
        self.SpawnTimer = 0

    def InitScene(self):

        # Load Textures
        self.System.LoadTextureToResources(os.path.dirname(__file__) + "/../res/Textures/player.png", 1, "playerShip")
        self.System.LoadTextureToResources(os.path.dirname(__file__) + "/../res/Textures/block.png", 0, "block")
        self.System.LoadTextureToResources(os.path.dirname(__file__) + "/../res/Textures/block_solid.png", 0,
                                           "block_solid")
        self.System.LoadTextureToResources(os.path.dirname(__file__) + "/../res/Textures/paddle.png", 1, "paddle")
        self.System.LoadTextureToResources(os.path.dirname(__file__) + "/../res/Textures/background.jpg", 0,
                                           "background")
        self.System.LoadTextureToResources(os.path.dirname(__file__) + "/../res/Textures/bg5.jpg", 0, "background2")
        self.System.LoadTextureToResources(os.path.dirname(__file__) + "/../res/Textures/sci_fi_bg1.jpg", 0,
                                           "background3")
        self.System.LoadTextureToResources(os.path.dirname(__file__) + "/../res/Textures/ball.png", 1, "ball")
        self.System.LoadTextureToResources(os.path.dirname(__file__) + "/../res/Textures/spikedball.png", 1,
                                           "spikedball")
        self.System.LoadTextureToResources(os.path.dirname(__file__) + "/../res/Textures/glasspaddle2.png", 1,
                                           "glasspaddle")
        self.System.LoadTextureToResources(os.path.dirname(__file__) + "/../res/Textures/particle.png", 1, "particle")
        self.System.LoadTextureToResources(os.path.dirname(__file__) + "/../res/Textures/cartoonship red.png", 1,
                                           "RedShip")
        self.System.LoadTextureToResources(os.path.dirname(__file__) + "/../res/Textures/DurrrSpaceShip.png", 1,
                                           "PlayerShip2")
        self.System.LoadTextureToResources(os.path.dirname(__file__) + "/../res/Textures/boss2.png", 1, "boss")

        self.player = Player()

        self.player.position = glm.vec2(self.System.windowWidth / 2 - Player_Size.x / 2,
                                        self.System.windowHeight / 2 - Player_Size.x / 2)
        self.player.Size = Player_Size
        self.player.Health = 3
        self.player.Texture = "PlayerShip2"

        self.background = "background2"
        self.ShipAmount = 15
        self.BossAmount = 15
        self.SceneWidth = self.System.windowWidth
        self.SceneHeight = self.System.windowHeight

    def Update(self, dt):
        self.ProccessInput(dt)
        # self.LevelList[self.CurrLevel].UpdateScene(1, dt)
        #
        # print(1/dt)
        self.UpdateScene(2, dt)

        self.player.UpdateProjectile(dt)
        self.DoCollision()
        self.CheckLoss()

    def UpdateScene(self, amount, dt):
        self.RemoveDead()

        for ship in self.gameObjects:
            ship.position = ship.position + (ship.Velocity * dt)

        if self.SpawnTimer >= 2:
            for x in range(0, amount):
                if self.ShipAmount > 0:
                    randPos = glm.vec2(random.uniform(150, self.SceneWidth - 150), 0.0)
                    size = glm.vec2(100, 100)
                    velocity = glm.vec2(0, 100)
                    NewShip = Ship()
                    NewShip.position = randPos
                    NewShip.Size = size
                    NewShip.Velocity = velocity
                    NewShip.Health = 3
                    NewShip.Texture = "RedShip"

                    self.gameObjects.append(NewShip)
                self.ShipAmount = self.ShipAmount - 1
            self.SpawnTimer = 0
        self.SpawnTimer = self.SpawnTimer + dt

    def Draw(self):
        self.StartScene(self.System, glm.vec3(0.6, 0.6, 1.0))
        for ship in self.gameObjects:
            ship.Draw(self.System)

        self.player.DrawProjectiles(self.System)
        self.player.Draw(self.System)

    def StartScene(self, system, backgroundColor):
        system.SystemDraw(self.System.GetTextureFromResources(self.background), glm.vec2(0, 0),
                          glm.vec2(self.SceneWidth, self.SceneHeight),
                          0.0, backgroundColor, glm.vec2(1, 1), glm.vec2(1, 1))

    def RemoveDead(self):
        Ind = 0
        for ship in self.gameObjects:
            if ship.Health <= 0:
                del self.gameObjects[Ind]
            Ind = Ind + 1

    def DelShip(self, Ind):
        del self.gameObjects[Ind]

    def DoCollision(self):
        ShipIndex = 0
        for ship in self.gameObjects:
            ProjectileIndex = 0
            for pro in self.player.ProjectileList:
                Collision = pro.DetectCollision(ship)
                if Collision:
                    self.player.DestroyProjectile(ProjectileIndex)
                    ship.Health = ship.Health - 1
                    ship.Color.x = ship.Color.x + 0.2
                ProjectileIndex = ProjectileIndex + 1

            Collision = self.player.DetectCollision(ship)
            if Collision:
                ship.Health = ship.Health - 1
                ship.Color.x = ship.Color.x + 0.2
            ShipIndex = ShipIndex + 1

    def CheckLoss(self):
        ShipIndex = 0
        for ship in self.gameObjects:
            if ship.position.y >= (self.SceneHeight + 50):
                self.player.Health = self.player.Health - 1
                self.DelShip(ShipIndex)
            ShipIndex = ShipIndex + 1
        if self.player.Health <= 0:
            print("GAME OVER")

    def ProccessInput(self, dt):
        keys = self.System.GetInput()

        self.player.Timer = self.player.Timer + dt
        Velocity = Player_Velocity * dt

        if keys[self.System.getKey("S")]:
            if self.player.position.y <= (self.SceneHeight - self.player.Size.y):
                self.player.position.y = self.player.position.y + Velocity

        if keys[self.System.getKey("W")]:
            if self.player.position.y >= 0:
                self.player.position.y = self.player.position.y - Velocity

        if keys[self.System.getKey("A")]:
            if self.player.position.x >= 0:
                self.player.position.x = self.player.position.x - Velocity

        if keys[self.System.getKey("D")]:
            if self.player.position.x <= (self.SceneWidth - self.player.Size.x):
                self.player.position.x = self.player.position.x + Velocity

        if keys[self.System.getKey("SPACE")]:
            self.player.MakeProjectile("ball", dt)
