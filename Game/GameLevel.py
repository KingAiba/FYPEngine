import glm
import os
import sys

# sys.path.append(os.path.dirname(__file__) + "/../")
sys.path.append(sys.path[0] + "/../")
from Game.GameObject import GameObject
from Game.GameObject import BallObject

from Source.System.LevelManager import LevelManager

Player_Size = glm.vec2(100, 20)
Player_Velocity = float(500.0)
Ball_Velocity = glm.vec2(100.0, -350.0)
Ball_Radius = 12.5

Time = 0.0


class GameLevel(LevelManager):
    def __init__(self, system):
        super(GameLevel, self).__init__(system)
        self.LevelsList = []
        self.CurrLevel = 0
        self.Blocks = []
        self.Player = None
        self.Ball = None
        # self.PGen = None

    def Load(self, FilePath, Width, Height):
        self.Blocks.clear()
        BlockData = []
        count = 0
        LevelFile = open(FilePath, "r")

        if not LevelFile:
            print("ERROR : CANNOT OPEN LEVEL FILE")
            return

        for line in LevelFile:
            # print(line)
            LineArray = line.split()
            count = count + len(LineArray)
            BlockData.append(LineArray)

        if count > 0:
            self.ConstructLevel(BlockData, Width, Height)

    def ConstructLevel(self, BlockData, LevelWidth, LevelHeight):

        height = len(BlockData)
        width = len(BlockData[0])

        UnitWidth = float(LevelWidth / width)
        UnitHeight = float(LevelHeight / height)
        IndexY = 0
        for y in BlockData:

            IndexX = 0
            for x in y:

                if int(x) == 1:
                    Pos = glm.vec2(UnitWidth * float(IndexX), UnitHeight * float(IndexY))
                    Size = glm.vec2(UnitWidth, UnitHeight)
                    Color = glm.vec3(0.9, 0.9, 0.9)

                    Obj = GameObject()
                    Obj.position = Pos
                    Obj.Size = Size
                    Obj.Color = Color
                    Obj.Texture = "block_solid"
                    Obj.IsSolid = True
                    self.Blocks.append(Obj)

                elif int(x) > 1:
                    color = glm.vec3(1.0, 1.0, 1.0)
                    Pos = glm.vec2(UnitWidth * float(IndexX), UnitHeight * float(IndexY))
                    Size = glm.vec2(UnitWidth, UnitHeight)

                    if int(x) == 2:
                        color = glm.vec3(0.0, 1.0, 1.3)
                    elif int(x) == 3:
                        color = glm.vec3(1.3, 1.0, 0.0)
                    elif int(x) == 4:
                        color = glm.vec3(0.5, 1.3, 0.0)
                    elif int(x) == 5:
                        color = glm.vec3(1.3, 0.3, 0.5)

                    Obj = GameObject()
                    Obj.position = Pos
                    Obj.Size = Size
                    Obj.Color = color
                    Obj.Texture = "block"
                    Obj.IsSolid = False
                    self.Blocks.append(Obj)

                IndexX = IndexX + 1
                # print(x, IndexX)

            IndexY = IndexY + 1
            # print(y, IndexY)

    def InitLevel(self):
        super().InitLevel()

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

        # make player object
        PlayerPos = glm.vec2(self.System.windowWidth / 2 - Player_Size.x / 2, self.System.windowHeight - Player_Size.y)
        self.Player = GameObject()
        self.Player.position = PlayerPos
        self.Player.Size = Player_Size
        self.Player.Texture = "glasspaddle"

        # make ball object
        BallPos = PlayerPos + glm.vec2(Player_Size.x / 2 - Ball_Radius, -Ball_Radius * 2)
        self.Ball = BallObject()
        self.Ball.position = BallPos
        self.Ball.Radius = Ball_Radius
        self.Ball.Size = glm.vec2(Ball_Radius * 2, Ball_Radius * 2)
        self.Ball.Velocity = Ball_Velocity
        self.Ball.Texture = "spikedball"

        # Load Levels
        self.Load(os.path.dirname(__file__) + "/levels/level0.txt", self.System.windowWidth,
                  self.System.windowHeight * 0.5)

    def Draw(self):
        self.System.SystemDraw(self.System.GetTextureFromResources("background3"), glm.vec2(0, 0),
                               glm.vec2(self.System.windowWidth, self.System.windowHeight), 0.0,
                               glm.vec3(0.3, 0.3, 0.5), glm.vec2(1, 1), glm.vec2(1, 1))
        for Tile in self.Blocks:
            if not Tile.Destroyed:
                Tile.Draw(self.System)
        self.Player.Draw(self.System)
        self.Ball.Draw(self.System)

    # self.PGen.Draw()

    def Update(self, dt):
        super().Update(dt)
        self.System.UpdateCamera(0, 0, 0, 0)
        self.ProccessInput(dt)
        # print(1/dt)
        self.Ball.BallMove(dt, self.System.windowWidth)
        self.BlockCollision()
        # self.PGen.Update(dt, self.Ball, 20, glm.vec2(self.Ball.Radius / 2))
        if self.Ball.position.y >= self.System.windowHeight:
            self.ResetLevel()
            self.ResetPlayer()
        if self.IsComplete():
            self.CurrLevel = self.CurrLevel + 1
            print(self.CurrLevel)
            if self.CurrLevel > 4:
                self.CurrLevel = 0
            self.ResetLevel()
            self.ResetPlayer()

    def ProccessInput(self, dt):
        Velocity = Player_Velocity * dt
        # print("DT : " + str(dt))
        # print("Velocity : " + str(Velocity))
        keys = self.System.GetInput()
        if keys[self.System.getKey("A")]:
            if self.Player.position.x >= 0:
                self.Player.position.x = self.Player.position.x - Velocity
                if self.Ball.Stuck:
                    self.Ball.position.x = self.Ball.position.x - Velocity

        if keys[self.System.getKey("D")]:
            if self.Player.position.x <= (self.System.windowWidth - self.Player.Size.x):
                self.Player.position.x = self.Player.position.x + Velocity
                if self.Ball.Stuck:
                    self.Ball.position.x = self.Ball.position.x + Velocity
        if keys[self.System.getKey("Q")]:
            for Tile in self.Blocks:
                if Tile.Destroyed is not True:
                    Tile.Destroyed = True

        if keys[self.System.getKey("SPACE")]:
            self.Ball.Stuck = False

    def IsComplete(self):
        for Tile in self.Blocks:
            if (not Tile.Destroyed) and (not Tile.IsSolid):
                return False
        return True

    def BlockCollision(self):
        # print(self.Ball.position)
        for Block in self.Blocks:
            if not Block.Destroyed:
                Collision = self.Ball.CheckClampedCollision(self.Ball, Block)

                if Collision[0]:
                    if not Block.IsSolid:
                        Block.Destroyed = True
                        # print(Block.Destroyed)
                    Direction = Collision[1]
                    diffVector = Collision[2]

                    if Direction == "LEFT" or Direction == "RIGHT":
                        self.Ball.Velocity.x = -self.Ball.Velocity.x
                        pen = self.Ball.Radius - abs(diffVector.x)
                        if Direction == "LEFT":
                            self.Ball.position.x = self.Ball.position.x + pen
                        else:
                            self.Ball.position.x = self.Ball.position.x - pen
                    else:
                        self.Ball.Velocity.y = -self.Ball.Velocity.y
                        pen = self.Ball.Radius - abs(diffVector.y)
                        if Direction == "UP":
                            self.Ball.position.y = self.Ball.position.y - pen
                        else:
                            self.Ball.position.y = self.Ball.position.y + pen

        Collision = self.Ball.CheckClampedCollision(self.Ball, self.Player)

        if not self.Ball.Stuck and Collision[0]:
            # check if player hits ball
            center = self.Player.position.x + self.Player.Size.x / 2
            distance = (self.Ball.position.x + self.Ball.Radius) - center
            disPercent = distance / (self.Player.Size.x / 2)

            strength = float(2.0)
            OldVel = self.Ball.Velocity
            self.Ball.Velocity.x = Ball_Velocity.x * disPercent * strength

            # self.Ball.Velocity.y = -self.Ball.Velocity.y
            self.Ball.Velocity.y = -1 * abs(self.Ball.Velocity.y)
            self.Ball.Velocity = glm.normalize(self.Ball.Velocity) * glm.length(OldVel)
            # print(self.Ball.Velocity)

    def ResetLevel(self):
        if self.CurrLevel == 0:
            self.Load(os.path.dirname(__file__) + "/levels/level0.txt", self.System.windowWidth,
                      self.System.windowHeight * 0.5)
        elif self.CurrLevel == 1:
            self.Load(os.path.dirname(__file__) + "/levels/level1.txt", self.System.windowWidth,
                      self.System.windowHeight * 0.5)
        elif self.CurrLevel == 2:
            self.Load(os.path.dirname(__file__) + "/levels/level2.txt", self.System.windowWidth,
                      self.System.windowHeight * 0.5)
        elif self.CurrLevel == 3:
            self.Load(os.path.dirname(__file__) + "/levels/level3.txt", self.System.windowWidth,
                      self.System.windowHeight * 0.5)

    def ResetPlayer(self):
        self.Player.Size = Player_Size
        PlayerPos = glm.vec2(self.System.windowWidth / 2 - Player_Size.x / 2, self.System.windowHeight - Player_Size.y)
        self.Player.position = PlayerPos
        self.Ball.Reset(PlayerPos + glm.vec2(Player_Size.x / 2 - Ball_Radius, -Ball_Radius * 2), Ball_Velocity)

# l = GameLevel()
# l.Load("levels/level1.txt", 1, 1)
