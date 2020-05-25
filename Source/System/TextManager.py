import glm
import sys
import os

sys.path.append(sys.path[0] + "/../../")
from Source.Utility.XmlUtility import GetRootAttribute
from Source.Renderer.ResourseManager import Resources
from Source.Renderer.texture import Texture

A = glm.vec2(6, 4)
B = glm.vec2(7, 4)
C = glm.vec2(8, 4)
D = glm.vec2(9, 4)
E = glm.vec2(10, 4)


# for text rendering
# default grid size 12 - 14
class TextManager:
    # initialize, (text sheet name, path to text sheet, path to xml containing text coordinates)
    def __init__(self, textsheet, textsheetPath, xmlPath):
        self.textSheet = textsheet
        self.textSheetPath = textsheetPath
        self.XML = xmlPath
        self.Text = ""
        self.position = glm.vec2(0, 0)
        self.size = glm.vec2(0, 0)
        self.rotation = float(0)
        self.color = glm.vec3(1.0, 1.0, 1.0)
        self.Grid = glm.vec2(12, 14)
        Resources.LoadTexture(textsheetPath, 1, textsheet)

    # get coord from xml for specified char
    def GetCoords(self, string):
        xStr = ""
        yStr = ""
        if not string.isalnum():
            xStr, yStr = self.checkSign(string)
        elif string.isnumeric():
            xStr = "x" + str(string)
            yStr = "y" + str(string)
            # print(xStr, yStr)
        else:
            xStr = string + "x"
            yStr = string + "y"

        coordX = (GetRootAttribute(self.GetPath() + self.XML, xStr))
        coordY = (GetRootAttribute(self.GetPath() + self.XML, yStr))
        if coordX is not None and coordY is not None:
            coordX = int(coordX)
            coordY = int(coordY)
        else:
            coordX = 1
            coordY = 1

        return coordX, coordY

    # draw string
    def DrawString(self, system, string, position=glm.vec2(0.0, 0.0), size=glm.vec2(24, 24),
                   color=glm.vec3(1.0, 1.0, 1.0)):
        count = 0
        for char in string:
            xStr, yStr = self.GetCoords(char)
            selected = glm.vec2(xStr, yStr)
            newPos = position.x
            newPos = newPos + (size.x * count)

            self.DrawChar(system, glm.vec2(newPos, position.y), size, self.rotation, color, self.Grid,
                          selected)
            count = count + 1

    # draw single char
    def DrawChar(self, system, position, size, rotate, color, Grid, Selected):
        system.SpriteRenderer.DrawSpriteFromSheet(Resources.Textures[self.textSheet], position, size, rotate, color,
                                                  Grid, Selected)

    @staticmethod
    def GetPath():
        return os.path.dirname(__file__) + "/../../res"

    # check for special characters in text, not fully implemented
    @staticmethod
    def checkSign(string):
        if string == ":":
            return "ColonX", "ColonY"

# t = TextManager("text", "/Text/8x8text_whiteNoShadow.png", "/Text/textCoord.xml")
# t.DrawString("sys", "SCORE:")
# t.GetPath()
