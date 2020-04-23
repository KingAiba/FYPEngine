# dictionary = {}
# print(dictionary)
# dictionary["New"] = "New"
# print(dictionary)

from Source.Renderer.Shader import Shader
from Source.Renderer.texture import Texture

from OpenGL.GL import *
from OpenGL.GLUT import *

from PIL import Image


class ResourceManager:

    def __init__(self):
        self.Textures = {}
        self.Shaders = {}

    def GetShader(self, Shader):
        return self.Shaders[Shader]

    def GetTexture(self, TexName):
        return self.Shaders[TexName]

    def LoadShader(self, VertexShaderFile, FragmentShaderFile, Name):
        NewShader = Shader(VertexShaderFile, FragmentShaderFile)
        self.Shaders[Name] = NewShader
        return NewShader

    def LoadTexture(self, File, Alpha, Name):
        self.Textures[Name] = self.TextureFromFile(File, Alpha)
        return self.Textures[Name]

    def TextureFromFile(self, File, Alpha):

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


Resources = ResourceManager()
