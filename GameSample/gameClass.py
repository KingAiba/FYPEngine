import glm
import os
import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
sys.path.append(os.path.dirname(__file__)+"/../../")

from Source.Renderer.BatchRenderer import BatchRenderer
from Source.Renderer.ResourseManager import Resources


Rows = 10
Cols = 10


class Game:
    def __init__(self, width, height, keys):
        self.width = width
        self.height = height
        self.keys = keys
        self.Renderer = None
        return

    def initial_renderer(self):
        Resources.LoadShader(os.path.dirname(__file__) + "/../../res/Shaders/BatchRenderVS2D.vs",
                             os.path.dirname(__file__) + "/../../res/Shaders/BatchRenderFS2D.fs", "Shader")
        Resources.LoadShader(os.path.dirname(__file__) + "/../../res/Shaders/VS2D.vs",
                             os.path.dirname(__file__) + "/../../res/Shaders/FS2D.fs", "Shader1")

        Resources.LoadTexture(os.path.dirname(__file__) + "/../../res/Textures/golem_attacking.png", 1,
                              "testTexture")
        Resources.LoadTexture(os.path.dirname(__file__) + "/../../res/Textures/spritesheet.png", 1,
                              "testTexture1")
        Resources.LoadTexture(os.path.dirname(__file__) + "/../../res/Textures/DurrrSpaceShip.png", 1,
                              "testTexture2")
        Resources.LoadTexture(os.path.dirname(__file__) + "/../../res/Textures/block.png", 0,
                              "block")
        # self.Renderer = SpriteRender(Resources.Shaders["Shader1"])
        self.Renderer = BatchRenderer(Resources.Shaders["Shader"])
        self.Renderer.Start()
        # Resources.Textures["testTexture"].FullGrid = glm.vec2(4, 3)

        projection = glm.ortho(0.0, self.width, self.height, 0.0, -1.0, 1.0)

        glUniformMatrix4fv(glGetUniformLocation(Resources.Shaders["Shader"].ID, "projection"), 1, GL_FALSE,
                           glm.value_ptr(projection))
        return

    def update(self, dt):
        print(dt ,1/dt)
        return

    def processInput(self, dt):
        return

    def render(self):
        unitX = self.width / Cols
        unitY = self.height / Rows
        i = 0
        while i < Rows:
            j = 0
            while j < Cols:
                self.Renderer.Draw(Resources.Textures["block"], glm.vec2(unitX * j, unitY * i),
                                    glm.vec2(unitX, unitY), 0.0, glm.vec3(1.0, 1.0, 1.0), glm.vec2(1, 1), glm.vec2(1, 1),
                                    1)
                j = j + 1
                # self.Renderer.DrawSprite(Resources.Textures["block"], glm.vec2(unitX * j, unitY * i),glm.vec2(unitX, unitY), 0.0, glm.vec3(1.0, 1.0, 1.0))

            i = i + 1

        self.Renderer.Render()
