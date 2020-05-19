import random
import glm
import numpy
from OpenGL.GL import *
from OpenGL.GLUT import *


class Particle:
    def __init__(self):
        self.Position = glm.vec2(0.0)
        self.Velocity = glm.vec2(0.0)
        self.Color = glm.vec4(1.0)
        self.Scale = float(6.0)
        self.Life = float(0.0)


class Generator:
    def __init__(self, shader, texture, amount):

        self.Shader = shader
        self.Texture = texture
        self.amount = amount
        self.VAO = GLuint(0)
        self.ParticleList = []
        self.LastUnused = 0

        self.InitRenderer()

    def Draw(self, system):
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        self.Shader.UseProgram()

        for particle in self.ParticleList:
            if particle.Life > 0.0:
                system.Camera.upload(self.Shader.ID, "projection")
                glUniform1f(glGetUniformLocation(self.Shader.ID, "Scale"), particle.Scale)
                glUniform2f(glGetUniformLocation(self.Shader.ID, "offset"), particle.position.x, particle.position.y)
                # print(particle.Position)
                glUniform4f(glGetUniformLocation(self.Shader.ID, "color"), particle.Color.x, particle.Color.y,
                            particle.Color.z, particle.Color.w)
                # print(particle.Color)
                self.Texture.BindTexture()
                glBindVertexArray(self.VAO)
                glDrawArrays(GL_TRIANGLES, 0, 6)
                glBindVertexArray(0)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def Update(self, dt, obj, particle, offset, r=1, g=1, b=1):
        # Add new from list, first unused particle

        for index in range(0, particle):

            Unused = self.FindUnusedParticle()

            self.RespawnParticle(self.ParticleList[Unused], obj, offset, r, g, b)

            Unused = self.FindUnusedParticle()

            self.RespawnParticle(self.ParticleList[Unused], obj, offset, r, g, b)

        for index in range(0, self.amount):
            P = self.ParticleList[index]
            P.Life = P.Life - dt*6

            if P.Life > 0.0:

                P.position = P.position - (P.Velocity * dt)
                P.Color.w = P.Color.w - dt*2
                # print(P.Color, P.Velocity, P.Position)

    def InitRenderer(self):
        self.Shader.Compile()
        self.Shader.UseProgram()

        VBO = GLuint(0)
        #                        //Pos    //Tex
        verticies = numpy.array([0.0, 1.0, 0.0, 1.0,
                                 1.0, 0.0, 1.0, 0.0,
                                 0.0, 0.0, 0.0, 0.0,

                                 0.0, 1.0, 0.0, 1.0,
                                 1.0, 1.0, 1.0, 1.0,
                                 1.0, 0.0, 1.0, 0.0], dtype="f")

        glGenVertexArrays(1, self.VAO)
        glGenBuffers(1, VBO)

        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, 4 * (numpy.size(verticies)), verticies, GL_STATIC_DRAW)
        glBindVertexArray(self.VAO)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, ctypes.sizeof(GLfloat) * 4, ctypes.c_void_p(0))
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        for i in range(self.amount):
            self.ParticleList.append(Particle())

    def FindUnusedParticle(self):

        for index in range(self.LastUnused, self.amount):
            if self.ParticleList[index].Life <= 0.0:
                self.LastUnused = index
                return index

        for index in range(0, self.LastUnused):
            if self.ParticleList[index].Life <= 0.0:
                self.LastUnused = index
                return index

        self.LastUnused = 0
        return 0

    @staticmethod
    def RespawnParticle(particle, obj, offset, r=1, g=1, b=1):
        randNum = (random.uniform(0, 100) - 50) / 10.0
        randColor = 0.5 + (random.uniform(0, 100) / 100.0)

        particle.position = obj.position + randNum + offset
        particle.Color = glm.vec4(randColor*r, randColor*g, randColor*b, 1.0)
        particle.Life = 1.0
        particle.Velocity = obj.Velocity * 0.1
