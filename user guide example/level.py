import os
import sys

# sys.path.append(os.path.dirname(__file__) + "/../")
from object import Player, Block
from Source.System.LevelManager import LevelManager
from Source.Utility.XmlUtility import PathToProject
from Source.System.TextManager import TextManager
from Source.System.audioManager import AudioManager
from Source.Renderer.ResourseManager import Resources
from Source.Utility.glmVec import GetVec2


class GameLevel(LevelManager):
    def __init__(self, system):
        super().__init__(system)
        self.player = None
        self.textManager = None
        self.audio = None
        self.PGen = None
        self.flag = 0
        self.timer = 0

    def InitLevel(self):
        super().InitLevel()
        self.player = Player(PathToProject() + "res/GameObjects/PlayerShip.xml")
        block1 = Block(PathToProject() + "res/GameObjects/block.xml")
        block2 = Block(PathToProject() + "res/GameObjects/block.xml")
        block2.position.x = 800

        self.textManager = TextManager("textsheet", "/Text/8x8text_whiteNoShadow.png", "/Text/textCoord.xml")

        self.audio = AudioManager()
        self.audio.LoadSound("/SoundEffects/scifi_weapon1.wav", "wep1")

        Resources.LoadTexture("/Textures/ball.png", 1, "particle")

        self.PGen = self.System.GetGenerator(Resources.GetTexture("particle"), 50)

        self.AddObject(block1)
        self.AddObject(block2)
        self.AddObject(self.player)

    def Update(self, dt):
        self.player.ProccessInput(dt, self.System)
        self.flag = 0
        for obj in self.gameObjects:

            if obj != self.player:
                if self.player.DetectCollision(obj):
                    self.flag = 1

                    if self.timer > 1:
                        self.audio.Play("wep1")
                        self.timer = 0
                    self.timer += dt
        self.System.UpdateCamera(self.player.position.x + self.player.Size.x / 2 - self.System.windowWidth / 2,
                                 self.player.position.y + self.player.Size.y / 2 - self.System.windowHeight / 2, 0, 0)
        super().Update(dt)
        self.PGen.Update(dt, self.player, 2, 10, GetVec2((self.player.position.x+self.player.Size.x/2)-10,
                                                         self.player.position.y+self.player.Size.y-20), 1.5, 0.5, 0.5)

    def Draw(self):
        self.PGen.Draw(self.System)
        if self.flag == 1:
            self.textManager.DrawString(self.System, "COLLISION")
        super().Draw()

