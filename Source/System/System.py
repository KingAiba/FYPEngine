import os
import sys
import glm
from OpenGL.GL import *

# sys.path.append(os.path.dirname(__file__) + "/../../")
sys.path.append(sys.path[0] + "/../../")

from Source.Renderer.ResourseManager import Resources
from Source.Renderer.SpriteRender import SpriteRender
from Source.Renderer.BatchRenderer import BatchRenderer
from Source.Renderer.ParticleSystem import Particle
from Source.Renderer.ParticleSystem import Generator
from Source.Renderer.windowManager import Window
from Source.Renderer.Camera2D import *
from Source.System.InputManager import *
from Source.Utility.XmlUtility import GetAttribute

window = Window()


class System:

    def __init__(self):
        self.windowWidth = 800
        self.windowHeight = 600
        self.windowTitle = None
        self.window = None
        self.SpriteRenderer = None
        self.BatchRenderer = None
        self.ParticleRenderer = None
        self.LevelManager = None
        self.InputManager = None
        self.Camera = None
        self.ConfigPath = os.path.dirname(__file__) + "/../../res/Config/SystemConfig.xml"

    def InitSystem(self):
        self.windowWidth = int(GetAttribute(self.ConfigPath, "Window", "windowWidth"))
        self.windowHeight = int(GetAttribute(self.ConfigPath, "Window", "windowHeight"))
        self.windowTitle = GetAttribute(self.ConfigPath, "Window", "windowTitle")

        self.window = window.CreateWindow(self.windowWidth, self.windowHeight, "Title")
        self.InputManager = InputManager()
        self.InputManager.SetCallback(self.window)

        # Resources.LoadShader(os.path.dirname(__file__) + "/../../res/Shaders/VS2D2.vs",
        #                      os.path.dirname(__file__) + "/../../res/Shaders/FS2D.fs", "Shader")
        Resources.LoadShader(os.path.dirname(__file__) + "/../../res/Shaders/VS2D2.vs",
                             os.path.dirname(__file__) + "/../../res/Shaders/FS2D2.fs", "ShaderV2")
        # Resources.LoadShader(os.path.dirname(__file__) + "/../../res/Shaders/ParticleVS.vs",
        #                      os.path.dirname(__file__) + "/../../res/Shaders/ParticleFS.fs", "ParticleShader")
        # Resources.LoadShader(os.path.dirname(__file__) + "/../../res/Shaders/BatchRenderVS2D.vs",
        #                      os.path.dirname(__file__) + "/../../res/Shaders/BatchRenderFS2D.fs", "BatchShader")

        self.SpriteRenderer = SpriteRender(Resources.Shaders["ShaderV2"])
        self.SpriteRenderer.initRenderer()

        self.Camera = Camera2D(0.0, self.windowWidth, self.windowHeight, 0.0)
        self.Camera.update(0.0, 0.0, 0.0)
        # projection = glm.ortho(0.0, self.windowWidth, self.windowHeight, 0.0, -1.0, 1.0)

        glUniformMatrix4fv(glGetUniformLocation(Resources.Shaders["Shader"].ID, "projection"), 1, GL_FALSE,
                           glm.value_ptr(self.Camera.VP))

        # self.BatchRenderer = BatchRenderer(Resources.Shaders["BatchShader"])
        # self.BatchRenderer.Start()
        # self.Camera.update(0.0, 0.0, 0.0)
        # glUniformMatrix4fv(glGetUniformLocation(Resources.Shaders["BatchShader"].ID, "projection"), 1, GL_FALSE,
        #                    glm.value_ptr(self.Camera.VP))

    def GameLoop(self, flag, r=0.3, g=0.2, b=0.6, a=1.0):

        if flag == 0:
            while not window.isWindowClosed():
                window.PollEvents()
                self.LevelManager.Update(self.GetDeltaTime())
                window.BackgroundColor(r, g, b, a)
                self.LevelManager.Draw()
                window.SwapBuffers()
        else:
            pass
            # while not window.isWindowClosed():
            #     window.PollEvents()
            #     self.LevelManager.Update(self.GetDeltaTime())
            #     window.BackgroundColor(r, g, b, a)
            #     self.LevelManager.BatchDraw()
            #     self.BatchRender()
            #     window.SwapBuffers()

    def ClearSystem(self):
        self.LevelManager.ClearLevel()

    def ChangeLevel(self, newLevel):
        self.LevelManager.ClearLevel()
        self.LevelManager = newLevel
        self.LevelManager.InitLevel()

    @staticmethod
    def GetDeltaTime():
        return window.GetDeltaTime()

    def GetInput(self):
        return self.InputManager.getKeys()

    def UpdateCamera(self, x, y, rotation, flag=0):
        if flag == 0:
            self.SpriteRenderer.shader.UseProgram()
            self.Camera.update(x, y, rotation)
            self.Camera.upload(self.SpriteRenderer.shader.ID, "projection")
        else:
            self.BatchRenderer.Shader.UseProgram()
            self.Camera.update(x, y, rotation)
            self.Camera.upload(self.BatchRenderer.Shader.ID, "projection")

    def getCameraPosition(self):
        return self.Camera.getPosition()

    def setCamera(self, left, right, bottom, top):
        self.Camera.setProjection(left, right, bottom, top)

    def getKey(self, key):
        return self.InputManager.key_string_to_glfw(key)

    def BatchRender(self):
        self.BatchRenderer.Render()

    @staticmethod
    def GetResourceManager():
        return Resources

    @staticmethod
    def LoadTextureToResources(texturePath, isAlpha, key):
        if key in Resources.Textures:
            pass
        else:
            Resources.LoadTexture(texturePath, isAlpha, key)


    @staticmethod
    def GetTextureFromResources(key):
        return Resources.Textures[key]

    @staticmethod
    def LoadShaderToResources(VertexShaderFile, FragmentShaderFile, key):
        if key in Resources.Shaders:
            pass
        else:
            Resources.LoadShader(VertexShaderFile, FragmentShaderFile, key)

    @staticmethod
    def GetShaderFromResources(key):
        return Resources.GetShader(key)

    def SystemDraw(self, texture, position, size, rotation, color, Grid, Selected):
        self.SpriteRenderer.DrawSpriteFromSheet(texture, position, size, rotation, color, Grid, Selected)

    def SystemTerminate(self):
        self.ClearSystem()
        self.SpriteRenderer = None
        self.BatchRenderer = None
        glfw.terminate()

# EngineSystem = System()
# EngineSystem.InitSystems()
# EngineSystem.GameLoop()
