import glm
from OpenGL.GL import *


class Texture:

    def __init__(self):
        self.ID = glGenTextures(1)
        self.Width = 0
        self.Height = 0
        self.Internal_Format = GL_RGB
        self.Image_Format = GL_RGB
        self.Wrap_S = GL_REPEAT
        self.Wrap_T = GL_REPEAT
        self.Filter_Min = GL_LINEAR
        self.Filter_Max = GL_LINEAR

    def Generate(self, width, height, data):
        self.Width = width
        self.Height = height

        glBindTexture(GL_TEXTURE_2D, self.ID)
        glTexImage2D(GL_TEXTURE_2D, 0, self.Internal_Format, width, height, 0, self.Image_Format, GL_UNSIGNED_BYTE,
                     data)

        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, self.Wrap_S)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, self.Wrap_T)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, self.Filter_Min)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, self.Filter_Max)

        glBindTexture(GL_TEXTURE_2D, 0)

    def BindTexture(self):
        glBindTexture(GL_TEXTURE_2D, self.ID)

    def BindTextureBySlot(self, slot):
        glActiveTexture(GL_TEXTURE0 + slot)
        glBindTexture(GL_TEXTURE_2D, self.ID)
        return self.ID

    def setTextureAttributes(self, Wrap_S, Wrap_T, Filter_Min, Filter_Max):
        self.Wrap_S = Wrap_S
        self.Wrap_T = Wrap_T
        self.Filter_Min = Filter_Min
        self.Filter_Max = Filter_Max

    @staticmethod
    def UnbindTexture():
        glBindTexture(GL_TEXTURE_2D, 0)

    @staticmethod
    def EnableAlpha():
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
