import glm
import os
import sys

# sys.path.append(os.path.dirname(__file__) + "/../../")
sys.path.append(sys.path[0] + "/../../")
from OpenGL.GL import *

class Camera2D:
    # initialize camera by setting camera dimensions
    def __init__(self, left, right, bottom, top):
        self.position = glm.vec3(0.0, 0.0, 0.0)
        self.rotation = float(0)
        self.scale = float(0.0)

        self.projectionMat = glm.ortho(left, right, bottom, top, -1.0, 1.0)
        self.viewMat = glm.mat4(1)
        self.VP = self.projectionMat * self.viewMat

        self.screenWidth = right
        self.screenHeight = bottom

    # change positions
    def setPosition(self, x, y):
        self.position.x = x
        self.position.y = y

    # change rotation
    def setRotation(self, rotation):
        self.rotation = rotation

    # getter functions
    def getRotation(self):
        return self.rotation

    def getPosition(self):
        return self.position

    # set scale
    def setScale(self, newScale):
        self.scale = newScale

    def getScale(self):
        return self.scale

    def getVP(self):
        return self.VP

    # set new projection matrix
    def setProjection(self, left, right, bottom, top):
        self.projectionMat = glm.ortho(left, right, bottom, top, -1.0, 1.0)

    def getProjection(self):
        return self.projectionMat

    def getView(self):
        return self.viewMat

    # recalculate view and projection-view matrix
    def CalcViewMatrix(self):
        transfrom = glm.translate(glm.mat4(1), self.position)
        transfrom = glm.rotate(transfrom, glm.radians(self.rotation), glm.vec3(0, 0, 1))

        self.viewMat = glm.inverse(transfrom)
        self.VP = self.projectionMat * self.viewMat

    # upload view-projection uniform to shader
    def upload(self, shaderID, uniform):
        glUniformMatrix4fv(glGetUniformLocation(shaderID, uniform), 1, GL_FALSE,
                           glm.value_ptr(self.VP))

    # update camera
    def update(self, x, y, rotation):
        self.setPosition(x, y)
        self.setRotation(rotation)
        self.CalcViewMatrix()
        # print(self.VP)



