import os
import sys

# sys.path.append(os.path.dirname(__file__) + "/../")
sys.path.append(sys.path[0] + "/../")
from Source.System.LevelManager import LevelManager
from Source.System.animationComponent import Animation
from Game3.GameObjects import Player
from Game3.GameObjects import Tile
from Source.Utility.glmVec import GetVec2, GetVec3

playerVelocity = float(250)


class GameLevel(LevelManager):

    def __init__(self, system):
        super().__init__(system)
        self.player = None
        self.staticObjects = []

    def InitLevel(self):
        super().InitLevel()
        # load resources
        self.System.LoadTextureToResources("/Textures/tile_spritesheet.png", 1, "TileSheet")
        self.System.LoadTextureToResources("/Text/8x8text_whiteNoShadow.png", 1, "textSheet")

        # init objects
        idleAnimation = Animation()
        idleAnimation.speed = 0.25
        idleAnimation.AnimationList = [GetVec2(1, 1), GetVec2(2, 1), GetVec2(3, 1), GetVec2(4, 1)]

        walkingAnimation = Animation()
        walkingAnimation.speed = 0.20
        walkingAnimation.AnimationList = [GetVec2(1, 2), GetVec2(2, 2), GetVec2(3, 2), GetVec2(4, 2),
                                          GetVec2(5, 2), GetVec2(6, 2)]

        jumpAnimation = Animation()
        jumpAnimation.speed = 0.15
        jumpAnimation.AnimationList = [GetVec2(7, 2), GetVec2(8, 2), GetVec2(1, 3), GetVec2(2, 3), GetVec2(3, 3),
                                       GetVec2(4, 3), GetVec2(5, 3), GetVec2(6, 3), GetVec2(7, 3), GetVec2(8, 3)]

        Player1 = Player(os.path.abspath(__file__) + "/../../res/GameObjects/Player.xml")

        Player1.Animated = True
        Player1.addAnimation(idleAnimation)
        Player1.addAnimation(walkingAnimation)
        Player1.addAnimation(jumpAnimation)
        Player1.position = GetVec2(530, 100)
        Player1.TexID = 0
        Player1.VerticalFlip = 1
        Player1.Velocity = GetVec2(0, 0)
        self.player = Player1

        testTile = Tile()
        testTile.position = GetVec2(500, 500)
        testTile.Size = GetVec2(100, 100)
        testTile.Grid = GetVec2(6, 4)
        testTile.Selected = GetVec2(3, 2)
        testTile.TexID = 1
        testTile.Texture = "TileSheet"

        testTile2 = Tile()
        testTile2.position = GetVec2(100, 500)
        testTile2.Size = GetVec2(200, 200)
        testTile2.Grid = GetVec2(6, 4)
        testTile2.Selected = GetVec2(3, 4)
        testTile2.TexID = 1
        testTile2.Texture = "TileSheet"

        testTile4 = Tile()
        testTile4.position = GetVec2(100, 100)
        testTile4.Size = GetVec2(100, 100)
        testTile4.Grid = GetVec2(6, 4)
        testTile4.Selected = GetVec2(2, 2)
        testTile4.TexID = 1
        testTile4.Texture = "TileSheet"


        testTile3 = Tile()
        testTile3.position = GetVec2(0, 0)
        testTile3.Size = GetVec2(50, 50)
        testTile3.Grid = GetVec2(12, 14)
        testTile3.Selected = GetVec2(6, 5)
        testTile3.TexID = 3
        testTile3.Texture = "textSheet"



        # self.AddObject(player)
        self.AddObject(Player1)
        self.AddObject(testTile2)
        self.AddObject(testTile3)
        self.AddObject(testTile4)
        self.AddObject(testTile)
        self.staticObjects.append(testTile)
        self.staticObjects.append(testTile2)
        self.staticObjects.append(testTile3)
        self.staticObjects.append(testTile4)

    def Update(self, dt):
        i = 0
        # print(self.player.Velocity)

        # print(self.System.GetDeltaTime())
        keys = self.System.GetInput()

        if keys[self.System.getKey("A")]:
            self.player.Velocity.x = -150
            self.player.VerticalFlip = 1
            i = 1

        if keys[self.System.getKey("D")]:
            self.player.Velocity.x = 150
            self.player.VerticalFlip = 0
            i = 1

        if keys[self.System.getKey("SPACE")]:
            self.player.jump()
            i = 2

        self.player.ChangeAnimationState(i)
        if not (keys[self.System.getKey("D")] or keys[self.System.getKey("A")]):
            self.player.Velocity.x = 0

        for Objects in self.staticObjects:
            if self.player.TileCollision(Objects):
                self.player.position.y = Objects.position.y - self.player.Size.y
                self.player.CollisionFlag = 1
                if not keys[self.System.getKey("SPACE")]:
                    self.player.JumpFlag = 0
                break
            else:
                self.player.CollisionFlag = 0

        super().Update(dt)

    def BatchDraw(self):
        super().BatchDraw()
