import os
import OpenGL.GL.shaders
from OpenGL.GL import *
from OpenGL.GLUT import *
import glfw


def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)


class Shader:
    def __init__(self, VSPath, FSPath):
        VSFile = open(VSPath, "r")
        FSFile = open(FSPath, "r")
        # check if file open
        if not VSFile:
            print("VERTEX SHADER NOT FOUND")
        if not FSFile:
            print("FRAGMENT SHADER NOT FOUND")
        # read and out shader code in member variables
        self.VSCode = VSFile.read() #VSFile.read()
        self.FSCode = FSFile.read()#FSFile.read()
        self.ID = 0

    def Compile(self):

        vertex = OpenGL.GL.shaders.compileShader(self.VSCode, GL_VERTEX_SHADER)
        frag = OpenGL.GL.shaders.compileShader(self.FSCode, GL_FRAGMENT_SHADER)

        # compile program
        self.ID = glCreateProgram();
        glAttachShader(self.ID, vertex)
        glAttachShader(self.ID, frag)
        glLinkProgram(self.ID)
        OpenGL.GL.shaders.compileProgram(vertex, frag)

        glDeleteShader(vertex)
        glDeleteShader(frag)

    def UseProgram(self):
        glUseProgram(self.ID)

    def GetUniformLocation(self, Uniform):
        return glGetUniformLocation(self.ID, Uniform)




# def main():
#     VSFILEPATH = os.path.dirname(__file__) + "/../../res/Shaders/VertexShader.vs"
#     FSFILEPATH = os.path.dirname(__file__) + "/../../res/Shaders/FragmentShader.fs"
#     shaderTest = Shader(VSFILEPATH, FSFILEPATH)
#     print(shaderTest.VSCode)
#     print(shaderTest.FSCode)
#
#     if not glfw.init():
#         return
#     # window creation create_window(width, height, monitor, shared)
#     width = 800
#     height = 600
#     window = glfw.create_window(width, height, "OpenGLProj", None, None)
#
#     # check if window is created
#     if not window:
#         # not created, program terminated
#         glfw.terminate()
#         return
#
#     # openGL context to draw in window
#     glfw.make_context_current(window)
#     glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
#     shaderTest.Compile()
#
#
# main()
