import numpy
import glm
from OpenGL.GL import *
from OpenGL.GLUT import *


class SpriteRender:
    def __init__(self, shader):
        self.shader = shader
        self.VAO = GLuint(0)

        self.initRenderer()

    #                    texClass   vec2    vec2   float   vec3
    def DrawSprite(self, texture, position, size, rotate, color):
        self.shader.UseProgram()

        model = glm.fmat4(1.0)
        model = glm.translate(model, glm.vec3(position, 0.0))

        model = glm.translate(model, glm.vec3(0.5 * size.x, 0.5 * size.y, 0.0))
        model = glm.rotate(model, rotate, glm.vec3(0.0, 0.0, 1.0))
        model = glm.translate(model, glm.vec3(-0.5 * size.x, -0.5 * size.y, 0.0))

        model = glm.scale(model, glm.vec3(size, 1.0))

        glUniformMatrix4fv(glGetUniformLocation(self.shader.ID, "model"), 1, GL_FALSE, glm.value_ptr(model))

        glUniform3f(glGetUniformLocation(self.shader.ID, "spriteColor"), color.x, color.y, color.z)

        glActiveTexture(GL_TEXTURE0)
        texture.BindTexture()

        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glBindVertexArray(0)

    def DrawSpriteFromSheet(self, texture, position, size, rotate, color, Grid, Selected):
        self.shader.UseProgram()

        model = glm.fmat4(1.0)
        model = glm.translate(model, glm.vec3(position, 0.0))

        model = glm.translate(model, glm.vec3(0.5 * size.x, 0.5 * size.y, 0.0))
        model = glm.rotate(model, rotate, glm.vec3(0.0, 0.0, 1.0))
        model = glm.translate(model, glm.vec3(-0.5 * size.x, -0.5 * size.y, 0.0))

        model = glm.scale(model, glm.vec3(size, 1.0))

        glUniformMatrix4fv(glGetUniformLocation(self.shader.ID, "model"), 1, GL_FALSE, glm.value_ptr(model))

        glUniform3f(glGetUniformLocation(self.shader.ID, "spriteColor"), color.x, color.y, color.z)
        glUniform2f(glGetUniformLocation(self.shader.ID, "FullGrid"), Grid.x, Grid.y)
        glUniform2f(glGetUniformLocation(self.shader.ID, "CurrCoord"), Selected.x, Selected.y)

        glActiveTexture(GL_TEXTURE0)
        texture.BindTexture()

        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glBindVertexArray(0)

    def initRenderer(self):
        self.shader.Compile()
        self.shader.UseProgram()

        VBO = GLuint(0)
        #                        //Pos    //Tex
        vertices = numpy.array([0.0, 1.0, 0.0, 1.0,
                                1.0, 0.0, 1.0, 0.0,
                                0.0, 0.0, 0.0, 0.0,

                                0.0, 1.0, 0.0, 1.0,
                                1.0, 1.0, 1.0, 1.0,
                                1.0, 0.0, 1.0, 0.0], dtype="f")
        glGenVertexArrays(1, self.VAO)
        glGenBuffers(1, VBO)

        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, 4 * (numpy.size(vertices)), vertices, GL_STATIC_DRAW)

        glBindVertexArray(self.VAO)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, ctypes.sizeof(GLfloat) * 4, ctypes.c_void_p(0))
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
