import os
import sys

# sys.path.append(os.path.dirname(__file__) + "/../")
sys.path.append(sys.path[0] + "/../")
from Source.System.LevelManager import LevelManager
from Source.System.animationComponent import Animation
from Game3.GameObjects import Player, Tile, Object
from Source.Utility.glmVec import GetVec2, GetVec3
from Source.Utility.XmlUtility import PathToProject
from Source.Renderer.ResourseManager import Resources

playerVelocity = float(250)


class GameLevel(LevelManager):

    def __init__(self, system):
        super().__init__(system)
        self.player = None
        self.staticObjects = []
        self.background = None
        self.Camera = None
        self.levelWidth = 1600
        self.levelHeight = 1600

    def InitLevel(self):
        super().InitLevel()
        # load resources
        Resources.LoadTexture("/Textures/tile_spritesheet.png", 1, "TileSheet")
        Resources.LoadTexture("/Textures/sci_fi_bg1.jpg", 0, "background")

        self.background = Object()
        self.background.position = GetVec2(0, 0)
        self.background.Size = GetVec2(self.levelWidth, self.levelHeight)
        self.background.Color = GetVec3(0.3, 0.3, 0.5)
        self.background.Texture = "background"
        self.background.TexID = 0

        self.Camera = self.System.Camera

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

        Player1 = Player(PathToProject() + "res/GameObjects/Player.xml")
        Player1.Animated = True
        Player1.addAnimation(idleAnimation)
        Player1.addAnimation(walkingAnimation)
        Player1.addAnimation(jumpAnimation)
        Player1.position = GetVec2(530, 100)
        Player1.TexID = 2
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

        # self.AddObject(player)
        self.AddObject(Player1)

        self.staticObjects.append(testTile)
        self.staticObjects.append(testTile2)
        self.MakeLevel("Game3/level1.txt", self.levelWidth, self.levelHeight)

    def Update(self, dt):
        i = 0
        # print(self.player.Velocity)
        self.System.UpdateCamera(self.player.position.x + self.player.Size.x/2 - self.System.windowWidth/2,
                                 self.player.position.y + self.player.Size.y/2 - self.System.windowHeight/2, 0, 1)
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
        self.background.BatchDraw(self.System)
        for obj in self.staticObjects:
            obj.BatchDraw(self.System)
        super().BatchDraw()

    def MakeLevel(self, filepath, width, height):
        filepath = PathToProject() + filepath
        count = 0
        BlockData = []
        file = open(filepath, "r")

        if not file:
            print("ERROR : CANNOT OPEN LEVEL FILE")
            exit()

        for line in file:
            # print(line)
            LineArray = line.split()
            count = count + len(LineArray)
            BlockData.append(LineArray)

        if count > 0:
            self.ConstructLevel(BlockData, width, height)

    def ConstructLevel(self, data, width, height):
        gapWidth = 64
        gapHeight = 64
        blockWidth = 125
        blockHeight = 64
        currPosx = 0
        currPosy = 0

        IndexY = 0
        for y in data:
            IndexX = 0
            for x in y:
                if int(x)==0:
                    currPosx=0
                elif int(x) == 1:
                    newTile = Tile(PathToProject() + "res/GameObjects/Tile1.xml")
                    newTile.TexID = 1
                    newTile.position = GetVec2(IndexX*gapWidth+currPosx, IndexY*gapHeight)
                    self.staticObjects.append(newTile)
                    currPosx += 61
                elif int(x) == 2:
                    newTile = Tile(PathToProject() + "res/GameObjects/Tile2.xml")
                    newTile.TexID = 1
                    newTile.position = GetVec2(IndexX*gapWidth+currPosx, IndexY*gapHeight)
                    self.staticObjects.append(newTile)
                    currPosx += 61
                elif int(x) == 3:
                    newTile = Tile(PathToProject() + "res/GameObjects/Tile2.xml")
                    newTile.TexID = 1
                    newTile.position = GetVec2(IndexX*gapWidth+currPosx, IndexY*gapHeight)
                    self.staticObjects.append(newTile)
                    currPosx += 61
                IndexX += 1
            IndexY += 1


