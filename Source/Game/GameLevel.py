import glm
from OpenGL.GL import *
from OpenGL.GLUT import *

from .GameObject import GameObject
from Renderer.ResourseManager import Resources


class GameLevel:
    def __init__(self):
        self.Blocks = []

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
            self.InitLevel(BlockData, Width, Height)

    def InitLevel(self, BlockData, LevelWidth, LevelHeight):

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
                    Obj.Position = Pos
                    Obj.Size = Size
                    Obj.Color = Color
                    Obj.Sprite = Resources.Textures["block_solid"]
                    Obj.IsSolid = GL_TRUE
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

                    Obj = GameObject();
                    Obj.Position = Pos
                    Obj.Size = Size
                    Obj.Color = color
                    Obj.Sprite = Resources.Textures["block"]
                    Obj.IsSolid = GL_FALSE
                    self.Blocks.append(Obj)

                IndexX = IndexX + 1
                # print(x, IndexX)

            IndexY = IndexY + 1
            # print(y, IndexY)

    def Draw(self, Renderer):
        for Tile in self.Blocks:
            if not Tile.Destroyed:
                Tile.Draw(Renderer)

    def IsComplete(self):
        for Tile in self.Blocks:
            if (not Tile.Destroyed) and (not Tile.IsSolid):
                return GL_FALSE
        return GL_TRUE

# l = GameLevel()
# l.Load("levels/level1.txt", 1, 1)
