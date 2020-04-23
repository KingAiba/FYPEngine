import glm
from OpenGL.GL import *
from OpenGL.GLUT import *
from Source.Renderer.ResourseManager import Resources
from Source.Renderer.SpriteRender import SpriteRender
from Source.Renderer.BatchRenderer import BatchRenderer



class Game:
    def __init__(self, width, height, keys):
        self.width = width
        self.height = height
        self.keys = keys
        self.Renderer = None
        return

    def initial_renderer(self):
        Resources.LoadShader(os.path.dirname(__file__) +"/../../res/Shaders/BatchRenderVS2D.vs",
                             os.path.dirname(__file__) +"/../../res/Shaders/BatchRenderFS2D.fs", "Shader")

        Resources.LoadTexture(os.path.dirname(__file__) + "/../../res/Textures/golem_attacking.png", 1,
                              "testTexture")
        self.Renderer = BatchRenderer()
        self.Renderer.Shader = Resources.Shaders["Shader"]
        self.Renderer.Start()
        Resources.Textures["testTexture"].FullGrid = glm.vec2(4, 3)

        projection = glm.ortho(0.0, self.width, self.height, 0.0, -1.0, 1.0)

        glUniformMatrix4fv(glGetUniformLocation(Resources.Shaders["Shader"].ID, "projection"), 1, GL_FALSE,
                           glm.value_ptr(projection))
        return

    def update(self, dt):  # dt = delta time
        print(1/dt)
        return

    def processInput(self, dt):
        return

    def render(self):
        self.Renderer.Draw(Resources.Textures["testTexture"], glm.vec2(0, 0),
                            glm.vec2(250, 150), 0.0, glm.vec3(1.0, 1.0, 1.0), glm.vec2(3, 4), glm.vec2(1, 1), 0)
        self.Renderer.Draw(Resources.Textures["testTexture"], glm.vec2(300, 0),
                           glm.vec2(250, 150), 0.0, glm.vec3(1.0, 1.0, 1.0), glm.vec2(3, 4), glm.vec2(3, 1), 0)
        self.Renderer.Draw(Resources.Textures["testTexture"], glm.vec2(0, 200),
                           glm.vec2(250, 150), 0.0, glm.vec3(1.0, 1.0, 1.0), glm.vec2(3, 4), glm.vec2(1, 4), 0)
        self.Renderer.Draw(Resources.Textures["testTexture"], glm.vec2(300, 200),
                           glm.vec2(250, 150), 0.0, glm.vec3(1.0, 1.0, 1.0), glm.vec2(3, 4), glm.vec2(2, 4), 0)

        self.Renderer.Render()
        return
