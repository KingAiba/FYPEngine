import random
import sys

sys.path.append(sys.path[0] + "/../")
from Game2.GameObjects import Ship
from Game2.GameObjects import Player
from Source.Renderer.ResourseManager import Resources
from Source.System.LevelManager import LevelManager
from Source.Utility.glmVec import GetVec2, GetVec3
from Source.System.TextManager import TextManager
from Source.System.audioManager import AudioManager
Player_Velocity = float(550.0)
Player_Size = GetVec2(125, 125)


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
        self.Txt = None
        self.audio = None

    def InitScene(self):

        # Load Textures
        Resources.LoadTexture("/Textures/player.png", 1, "playerShip")
        Resources.LoadTexture("/Textures/block.png", 0, "block")
        Resources.LoadTexture("/Textures/block_solid.png", 0, "block_solid")
        Resources.LoadTexture("/Textures/paddle.png", 1, "paddle")
        Resources.LoadTexture("/Textures/background.jpg", 0, "background")
        Resources.LoadTexture("/Textures/bg5.jpg", 0, "background2")
        Resources.LoadTexture("/Textures/sci_fi_bg1.jpg", 0, "background3")
        Resources.LoadTexture("/Textures/ball.png", 1, "ball")
        Resources.LoadTexture("/Textures/spikedball.png", 1, "spikedball")
        Resources.LoadTexture("/Textures/glasspaddle2.png", 1, "glasspaddle")
        Resources.LoadTexture("/Textures/particle.png", 1, "particle")
        Resources.LoadTexture("/Textures/cartoonship red.png", 1, "RedShip")
        Resources.LoadTexture("/Textures/DurrrSpaceShip.png", 1, "PlayerShip2")
        Resources.LoadTexture("/Textures/boss2.png", 1, "boss")

        self.player = Player()

        self.player.position = GetVec2(self.System.windowWidth / 2 - Player_Size.x / 2,
                                       self.System.windowHeight / 2 - Player_Size.x / 2)
        self.player.Size = Player_Size
        self.player.Health = 3
        self.player.Texture = "PlayerShip2"
        self.player.Velocity = Player_Velocity

        self.background = "background2"
        self.ShipAmount = 15
        self.BossAmount = 15
        self.SceneWidth = self.System.windowWidth
        self.SceneHeight = self.System.windowHeight

        self.Txt = TextManager("textsheet", "/Text/8x8text_whiteNoShadow.png", "/Text/textCoord.xml")
        self.Txt.position = GetVec2(0, 0)
        self.Txt.size = GetVec2(24, 24)

        self.audio = AudioManager()
        self.audio.LoadSound("/SoundEffects/scifi_weapon1.wav", "wep1")
        self.audio.LoadSound("/SoundEffects/NewHorizons.wav", "music1")


    def Update(self, dt):
        self.player.Update(dt, self.System, self.audio)
        # self.LevelList[self.CurrLevel].UpdateScene(1, dt)
        #
        # print(1/dt)
        self.UpdateScene(2, dt)
        self.audio.LoopPlay("music1")
        self.DoCollision()
        self.CheckLoss()

    def UpdateScene(self, amount, dt):
        self.RemoveDead()

        for ship in self.gameObjects:
            ship.position = ship.position + (ship.Velocity * dt)

        if self.SpawnTimer >= 2:
            for x in range(0, amount):
                if self.ShipAmount > 0:
                    randPos = GetVec2(random.uniform(150, self.SceneWidth - 150), 0.0)
                    size = GetVec2(100, 100)
                    velocity = GetVec2(0, 100)
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
        self.StartScene(self.System, GetVec3(0.6, 0.6, 1.0))
        self.player.Draw(self.System)
        super().Draw()
        self.Txt.DrawString(self.System, "SCORE:8317")

    def StartScene(self, system, backgroundColor):
        system.SystemDraw(Resources.GetTexture(self.background), GetVec2(0, 0),
                          GetVec2(self.SceneWidth, self.SceneHeight),
                          0.0, backgroundColor, GetVec2(1, 1), GetVec2(1, 1))

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
