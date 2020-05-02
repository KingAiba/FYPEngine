import os

import glm
from OpenGL.GL import *

from Renderer.ResourseManager import Resources
from Renderer.SpriteRender import SpriteRender
from Renderer.windowManager import Window
from .InputManager import InputManager
from Utility.XmlUtility import GetAttribute

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
        self.ConfigPath = os.path.dirname(__file__) + "/../../res/Config/SystemConfig.xml"

    def InitSystems(self):
        self.windowWidth = int(GetAttribute(self.ConfigPath, "Window", "windowWidth"))
        self.windowHeight = int(GetAttribute(self.ConfigPath, "Window", "windowHeight"))
        self.windowTitle = GetAttribute(self.ConfigPath, "Window", "windowTitle")

        self.window = window.CreateWindow(self.windowWidth, self.windowHeight, "Title")
        self.InputManager = InputManager()
        self.InputManager.SetCallback(self.window)

        Resources.LoadShader(os.path.dirname(__file__) + "/../../res/Shaders/VS2D2.vs",
                             os.path.dirname(__file__) + "/../../res/Shaders/FS2D.fs", "Shader")
        Resources.LoadShader(os.path.dirname(__file__) + "/../../res/Shaders/ParticleVS.vs",
                             os.path.dirname(__file__) + "/../../res/Shaders/ParticleFS.fs", "ParticleShader")
        Resources.LoadShader(os.path.dirname(__file__) + "/../../res/Shaders/BatchRenderVS2D.vs",
                             os.path.dirname(__file__) + "/../../res/Shaders/BatchRenderFS2D.fs", "BatchShader")


        # print(Resources.Shaders["Shader"])
        self.SpriteRenderer = SpriteRender(Resources.Shaders["Shader"])
        self.SpriteRenderer.initRenderer()

        projection = glm.ortho(0.0, self.windowWidth, self.windowHeight, 0.0, -1.0, 1.0)

        glUniformMatrix4fv(glGetUniformLocation(Resources.Shaders["Shader"].ID, "projection"), 1, GL_FALSE,
                           glm.value_ptr(projection))

    def GameLoop(self):
        while not window.isWindowClosed():
            window.PollEvents()
            self.LevelManager.Update()
            window.BackgroundColor(0.2, 0.2, 0.4, 1.0)
            self.LevelManager.Draw()
            window.SwapBuffers()

    def ClearSystem(self):
        self.LevelManager.ClearLevel()


    def ChangeLevel(self, newLevel):
        self.LevelManager.ClearLevel()
        self.LevelManager = newLevel
        self.LevelManager.InitLevel()

    @staticmethod
    def GetDeltaTime():
        return window.GetDeltaTime()

    def GetKeys(self):
        return self.InputManager.getKeys()


# EngineSystem = System()
# EngineSystem.InitSystems()
# EngineSystem.GameLoop()
