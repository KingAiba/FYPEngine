import glm
from Source.Utility.XmlUtility import GetAttribute
from Source.Renderer.ResourseManager import Resources

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

        if FilePath is not None:
            self.GetAttrFromFile(FilePath)

    def Update(self):
        return

    def Move(self, dt):
        self.position = self.position + (self.Velocity * dt)

        return self.position

    def Draw(self, system):
        system.SpriteRenderer.DrawSpriteFromSheet(Resources.Textures[self.Texture], self.position, self.Size,
                                                        self.Rotation, self.Color, self.Grid, self.Selected)

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
