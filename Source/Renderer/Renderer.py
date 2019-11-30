from OpenGL.GL import *

class Renderer:
    def __init__(self, name):
        self.name = name


    def Clear(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def ClearColor(self, r, g, b, a):
        glClearColor(r, g, b, a)

    def GetAttribLocation(self, shader, name):
        return glGetAttribLocation(shader, name)

    def VertexAttribPointer(self, location, size, type, normalized, stride, voidPointer):
        glVertexAttribPointer(location, size, type, normalized, stride, voidPointer)

    def EnableVertexArribArray(self, location):
        glEnableVertexAttribArray(location)

    def DisableVertexArribArray(self, location):
        glDisableVertexAttribArray(location)

    def DrawArrays(self, Mode, Index, Size):
        glDrawArrays(Mode, Index, Size)

    def GenBuffer(self, size):
        return glGenBuffers(size)

    def BindBuffer(self, target, buffer):
        glBindBuffer(target, buffer)

    def BufferData(self, target, size, data, mode):
        glBufferData(target, size, data, mode)
