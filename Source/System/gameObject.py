import glm
import os
import sys

# sys.path.append(os.path.dirname(__file__) + "/../../")
sys.path.append(sys.path[0] + "/../../")

from Source.Utility.XmlUtility import GetAttribute
from Source.Renderer.ResourseManager import Resources


# python game engine, wrapper, use does need to deal with the complxity of libraries,
# advantages to using engine
# installation, new project, simple game

# PathToTexture = "../"


class Sprite:

    def __init__(self, FilePath=None):
        self.position = glm.vec2(0.0, 0.0)
        self.Size = glm.vec2(1, 1)
        self.Rotation = 0.0
        self.Velocity = glm.vec2(0.0, 0.0)
        self.Color = glm.vec3(1.0, 1.0, 1.0)
        self.Alpha = 1.0
        self.Texture = ""
        self.Grid = glm.vec2(1, 1)
        self.Selected = glm.vec2(1, 1)
        self.VerticalFlip = 0
        self.HorizontalFlip = 0
        self.TexID = 0
        self.Animated = False
        self.Animations = []
        self.AnimationState = 0
        self.ObjectType = "STATIC"

        if FilePath is not None:
            self.GetAttrFromFile(FilePath)

    def Update(self, dt):
        pass

    def Move(self, dt):
        self.position = self.position + (self.Velocity * dt)
        return self.position

    def MoveX(self, dt, velx):
        self.position.x = self.position.x + (velx * dt)
        return self.position.x

    def MoveY(self, dt, vely):
        self.position.y = self.position.y + (vely * dt)
        return self.position.y

    # use sprite renderer
    def Draw(self, system):
        system.SpriteRenderer.DrawSpriteFromSheet(Resources.Textures[self.Texture], self.position, self.Size,
                                                  self.Rotation, self.Color, self.Grid, self.Selected)

    # use batch renderer
    def BatchDraw(self, system):
        system.BatchRenderer.Draw(Resources.Textures[self.Texture], self.position, self.Size,
                                  self.Rotation, self.Color, self.Grid, self.Selected, self.TexID,
                                  self.VerticalFlip)

    def GetAttrFromFile(self, FilePath):
        self.position.x = float(GetAttribute(FilePath, "Transform", "PosX"))
        self.position.y = float(GetAttribute(FilePath, "Transform", "PosY"))
        self.Rotation = float(GetAttribute(FilePath, "Transform", "rotation"))
        self.Size.x = float(GetAttribute(FilePath, "Transform", "sizeX"))
        self.Size.y = float(GetAttribute(FilePath, "Transform", "sizeY"))

        self.Color.x = float(GetAttribute(FilePath, "Sprite", "ColorR"))
        self.Color.y = float(GetAttribute(FilePath, "Sprite", "ColorG"))
        self.Color.z = float(GetAttribute(FilePath, "Sprite", "ColorB"))
        self.Alpha = float(GetAttribute(FilePath, "Sprite", "Alpha"))
        self.Texture = GetAttribute(FilePath, "Sprite", "textureName")

        self.Grid.x = int(GetAttribute(FilePath, "Sprite", "GridX"))
        self.Grid.y = int(GetAttribute(FilePath, "Sprite", "GridY"))

        self.Selected.x = int(GetAttribute(FilePath, "Sprite", "SelectedX"))
        self.Selected.y = int(GetAttribute(FilePath, "Sprite", "SelectedY"))

        isAlpha = int(GetAttribute(FilePath, "Sprite", "isAlpha"))
        if self.Texture in Resources.Textures:
            pass
        else:
            Resources.LoadTexture(GetAttribute(FilePath, "Sprite", "texturePath"), isAlpha, self.Texture)

    def DetectCollision(self, gameObject):
        ColX = False
        ColY = False

        if ((self.position.x + self.Size.x) >= gameObject.position.x) and (
                (gameObject.position.x + gameObject.Size.x) >= self.position.x):
            ColX = True
        if ((self.position.y + self.Size.y) >= gameObject.position.y) and (
                (gameObject.position.y + gameObject.Size.y) >= self.position.y):
            ColY = True

        return ColX and ColY

    # check direction of collision
    @staticmethod
    def CheckDirection(target):
        compass = [glm.vec2(0.0, 1.0), glm.vec2(1.0, 0.0), glm.vec2(0.0, -1.0), glm.vec2(-1.0, 0.0)]
        direction = ["UP", "RIGHT", "DOWN", "LEFT"]

        maxVal = 0.0
        bestVal = -1
        index = 0

        for value in compass:
            dotProduct = glm.dot(glm.normalize(target), value)

            if dotProduct > maxVal:
                maxVal = dotProduct
                bestVal = index

            index = index + 1

        return direction[bestVal]

    # check clamped collision
    def CheckClampedCollision(self, Obj1, Obj2):
        # find center of call
        center = glm.vec2(Obj1.position + Obj1.Radius)

        # calculate halk extents
        halfExtent = glm.vec2(Obj2.Size.x / 2, Obj2.Size.y / 2)
        aabbCenter = glm.vec2(Obj2.position.x + halfExtent.x, Obj2.position.y + halfExtent.y)

        # get difference and clamped val
        difference = center - aabbCenter
        clamped = glm.clamp(difference, -halfExtent, halfExtent)
        closest = aabbCenter + clamped
        difference = closest - center

        if glm.length(difference) < Obj1.Radius:
            Collision = (True, self.CheckDirection(difference), difference)
        else:
            Collision = (False, "UP", glm.vec2(0, 0))

        return Collision

    # getter and setter functions
    def getPosition(self):
        return self.position

    def setPosition(self, x, y):
        self.position.x = x
        self.position.y = y

    def getRotation(self):
        return self.Rotation

    def setRotation(self, rotation):
        self.Rotation = rotation

    def getSize(self):
        return self.Size

    def setSize(self, width, height):
        self.Size.x = width
        self.Size.y = height

    def getVelocity(self):
        return self.Velocity

    def setVelocity(self, x, y):
        self.Velocity.x = x
        self.Velocity.y = y

    def GetTexture(self):
        return Resources.Textures[self.Texture]

    def GetRGB(self):
        return self.Color

    def SetRGB(self, R, G, B):
        self.Color.x = R
        self.Color.y = G
        self.Color.z = B

    def GetAlpha(self):
        return self.Alpha

    def SetAlpha(self, alpha):
        self.Alpha = alpha

    def SetGrid(self, x, y):
        self.Grid.x = x
        self.Grid.y = y

    def getGrid(self):
        return self.Grid

    def SetSelected(self, x, y):
        self.Selected.x = x
        self.Selected.y = y

    def getSelected(self):
        return self.Selected

    def addAnimation(self, newAnimation):
        self.Animations.append(newAnimation)

    def playAnimation(self, dt):
        if self.Animated:
            self.Selected = self.Animations[self.AnimationState].Play(dt)
            # print(self.Selected)

    def ChangeAnimationState(self, state):
        self.AnimationState = state

    def setTexture(self, key):
        self.Texture = key

    def setNewTexture(self, texturePath, isAlpha, key):
        if key in Resources.Textures:
            pass
        else:
            Resources.LoadTexture(texturePath, isAlpha, key)

        self.Texture = key
