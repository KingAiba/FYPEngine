# dictionary = {}
# print(dictionary)
# dictionary["New"] = "New"
# print(dictionary)
import os
import sys
# sys.path.append(os.path.dirname(__file__)+"/../../")
sys.path.append(sys.path[0] + "/../../")

from Source.Renderer.Shader import Shader
from Source.Renderer.texture import Texture

from OpenGL.GL import *
from PIL import Image


class ResourceManager:

    def __init__(self):
        self.Textures = {}
        self.Shaders = {}

    def GetShader(self, Shader):
        return self.Shaders[Shader]

    def GetTexture(self, TexName):
        return self.Textures[TexName]

    def LoadShader(self, VertexShaderFile, FragmentShaderFile, Name):
        NewShader = Shader(self.GetAssetPath() + VertexShaderFile, self.GetAssetPath() + FragmentShaderFile)
        self.Shaders[Name] = NewShader
        return NewShader

    def LoadTexture(self, File, Alpha, Name):
        self.Textures[Name] = self.TextureFromFile(self.GetAssetPath() + File, Alpha)
        return self.Textures[Name]

    @staticmethod
    def TextureFromFile(File, Alpha):

        ImageSource = Image.open(File)

        if not ImageSource:
            print("ERROR: IMAGE NOT FOUND")
            return 0

        texture = Texture()
        if Alpha:
            texture.Internal_Format = GL_RGBA
            texture.Image_Format = GL_RGBA
            texture.EnableAlpha()
        #     ImageSource = ImageSource.covert("RGBA")
        #
        # else:
        #     ImageSource = ImageSource.covert("RGB")

        ImageArray = ImageSource.tobytes()
        ImgWidth, ImgHeight = ImageSource.size
        texture.Generate(ImgWidth, ImgHeight, ImageArray)

        return texture

    @staticmethod
    def GetAssetPath():
        # print(os.path.dirname(__file__) + "/../../res")
        return os.path.dirname(__file__) + "/../../res"

    def clear(self):
        self.Textures.clear()
        self.Shaders.clear()
Resources = ResourceManager()
