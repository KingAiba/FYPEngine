import numpy
import glm
import os
import sys
import _ctypes
from OpenGL.GL import *
from OpenGL.GLUT import *
sys.path.append(os.path.dirname(__file__)+"/../../")
from Source.Renderer.texture import Texture


#                         x   y    color        tx   ty   ti
sampleQuad = numpy.array([0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1,
                          1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1,
                          0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1,

                          0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1,
                          1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1,
                          1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1], dtype="f")


class BatchRenderer:
    def __init__(self):
        self.Shader = None
        self.VAO = GLuint(0)
        self.VBO = GLuint(0)
        self.Objects = []
        self.MaxObjects = 100
        self.MaxTexture = 30
        self.TextureIndex = 0
        self.Textures = [None] * self.MaxTexture
        self.BufferSize = numpy.size(sampleQuad) * self.MaxObjects * 4

    def AddObject(self, position, size, rotation, grid, selected):
        return

    def Start(self):
        self.Shader.Compile()
        self.Shader.UseProgram()

        glGenVertexArrays(1, self.VAO)
        glGenBuffers(1, self.VBO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.BufferSize, ctypes.c_void_p(0), GL_DYNAMIC_DRAW)

        glBindVertexArray(self.VAO)
        # position attribute
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, ctypes.sizeof(GLfloat) * 8, ctypes.c_void_p(0))
        # color
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, ctypes.sizeof(GLfloat) * 8,
                              ctypes.c_void_p(2 * ctypes.sizeof(GLfloat)))
        # tex
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, ctypes.sizeof(GLfloat) * 8,
                              ctypes.c_void_p(5 * ctypes.sizeof(GLfloat)))
        # texID
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 1, GL_FLOAT, GL_FALSE, ctypes.sizeof(GLfloat) * 8,
                              ctypes.c_void_p(7 * ctypes.sizeof(GLfloat)))

    # TODO fix texture slot inconsistency
    def Render(self):
        IDarray = [None] * self.MaxTexture
        count = 0
        for texture in self.Textures:
            if texture is None:
                break
            IDarray[count] = texture.BindTextureBySlot(count)
            # print(self.Textures)
            # print(IDarray[count])
            count = count + 1

        glUniform1iv(self.Shader.GetUniformLocation("Textures"), count, IDarray[:count])
        # print(IDarray[:count])
        while self.Objects:
            count = 0
            CurrDrawArray = numpy.array([], dtype="f")
            for obj in self.Objects:
                if count >= self.MaxObjects:
                    break
                CurrDrawArray = numpy.append(CurrDrawArray, obj)
                count = count + 1

            sizeOfData = numpy.size(CurrDrawArray) * 4
            glBufferSubData(GL_ARRAY_BUFFER, 0, sizeOfData, CurrDrawArray)

            glBindVertexArray(self.VAO)
            glDrawArrays(GL_TRIANGLES, 0, numpy.size(CurrDrawArray))
            # glClearBufferData(GL_ARRAY_BUFFER, GL_FLOAT, GL_FLOAT, GL_FLOAT, ctypes.c_void_p(0))
            glBindVertexArray(0)
            del self.Objects[:count]
            # print("Batch Done at : " + str(count))
        self.End()

    def Draw(self, texture, position, size, rotate, color, grid, selected, TexID):
        model = glm.fmat4(1.0)
        model = glm.translate(model, glm.vec3(position, 0.0))

        model = glm.translate(model, glm.vec3(0.5 * size.x, 0.5 * size.y, 0.0))
        model = glm.rotate(model, rotate, glm.vec3(0.0, 0.0, 1.0))
        model = glm.translate(model, glm.vec3(-0.5 * size.x, -0.5 * size.y, 0.0))

        model = glm.scale(model, glm.vec3(size, 1.0))

        glPos1 = model * glm.vec4(0.0, 1.0, 0.0, 1.0)
        glPos2 = model * glm.vec4(1.0, 0.0, 0.0, 1.0)
        glPos3 = model * glm.vec4(0.0, 0.0, 0.0, 1.0)
        glPos4 = model * glm.vec4(1.0, 1.0, 0.0, 1.0)

        # Pos                 color                            TexCoords                                    TexID
        vertices = numpy.array(
            [glPos1.x, glPos1.y, color.x, color.y, color.z, ((selected.x - 1) / grid.x), (selected.y / grid.y), TexID,
             glPos2.x, glPos2.y, color.x, color.y, color.z, (selected.x / grid.x), ((selected.y - 1) / grid.y), TexID,
             glPos3.x, glPos3.y, color.x, color.y, color.z, ((selected.x - 1) / grid.x), ((selected.y - 1) / grid.y),
             TexID,

             glPos1.x, glPos1.y, color.x, color.y, color.z, ((selected.x - 1) / grid.x), (selected.y / grid.y), TexID,
             glPos4.x, glPos4.y, color.x, color.y, color.z, (selected.x / grid.x), (selected.y / grid.y), TexID,
             glPos2.x, glPos2.y, color.x, color.y, color.z, (selected.x / grid.x), ((selected.y - 1) / grid.y), TexID],
            dtype="f")

        if self.TextureIndex >= self.MaxTexture:
            print("ERROR : Texture binding limit reached, currently set at : " + str(self.MaxTexture))
            exit()

        if (texture not in self.Textures) and (self.TextureIndex < self.MaxTexture):
            self.Textures[self.TextureIndex] = texture
            self.TextureIndex = self.TextureIndex + 1

        self.Objects.append(vertices)

    def End(self):
        self.Objects.clear()
        self.Textures = [None] * self.MaxTexture
        self.TextureIndex = 0

# int index = int(TexID);
#     if(index == 0){
#         color = vec4(1.0, 0.0, 0.0, 1.0)*texture(Textures[index], TexCoords);
#     }else if(index == 1){
#         color = vec4(0.0, 1.0, 0.0, 1.0)*texture(Textures[index], TexCoords);
#     }else if(index == 2){
#         color = vec4(0.0, 0.0, 1.0, 1.0)*texture(Textures[index], TexCoords);
#     }
