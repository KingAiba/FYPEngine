import OpenGL.GL.shaders
from OpenGL.GL import *


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
        self.VSCode = VSFile.read()  # VSFile.read()
        self.FSCode = FSFile.read()  # FSFile.read()
        self.ID = 0
    # compile vs and fs before rendering
    def Compile(self):

        vertex = OpenGL.GL.shaders.compileShader(self.VSCode, GL_VERTEX_SHADER)
        frag = OpenGL.GL.shaders.compileShader(self.FSCode, GL_FRAGMENT_SHADER)

        # compile program
        self.ID = glCreateProgram()
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
    # get uniform functions
    @staticmethod
    def GetUniform1f(uniform, v0):
        return glUniform1f(glGetUniformLocation(uniform), v0)

    @staticmethod
    def GetUniform2f(uniform, v0, v1):
        return glUniform2f(glGetUniformLocation(uniform), v0, v1)

    @staticmethod
    def GetUniform3f(uniform, v0, v1, v2):
        return glUniform3f(glGetUniformLocation(uniform), v0, v1, v2)

    @staticmethod
    def GetUniform4f(uniform, v0, v1, v2, v3):
        return glUniform4f(glGetUniformLocation(uniform), v0, v1, v2, v3)

    @staticmethod
    def GetUniform1i(uniform, v0):
        return glUniform1i(glGetUniformLocation(uniform), v0)

    @staticmethod
    def GetUniform2i(uniform, v0, v1):
        return glUniform2i(glGetUniformLocation(uniform), v0, v1)

    @staticmethod
    def GetUniform3i(uniform, v0, v1, v2):
        return glUniform3i(glGetUniformLocation(uniform), v0, v1, v2)

    @staticmethod
    def GetUniform4i(uniform, v0, v1, v2, v3):
        return glUniform4i(glGetUniformLocation(uniform), v0, v1, v2, v3)

    @staticmethod
    def GetUniform1ui(uniform, v0):
        return glUniform1ui(glGetUniformLocation(uniform), v0)

    @staticmethod
    def GetUniform2ui(uniform, v0, v1):
        return glUniform2ui(glGetUniformLocation(uniform), v0, v1)

    @staticmethod
    def GetUniform3ui(uniform, v0, v1, v2):
        return glUniform3ui(glGetUniformLocation(uniform), v0, v1, v2)

    @staticmethod
    def GetUniform4ui(uniform, v0, v1, v2, v3):
        return glUniform4ui(glGetUniformLocation(uniform), v0, v1, v2, v3)

    @staticmethod
    def GetUniform1fv(uniform, count, val):
        return glUniform1fv(glGetUniformLocation(uniform), count, val)

    @staticmethod
    def GetUniform2fv(uniform, count, val):
        return glUniform2fv(glGetUniformLocation(uniform), count, val)

    @staticmethod
    def GetUniform3fv(uniform, count, val):
        return glUniform3fv(glGetUniformLocation(uniform), count, val)

    @staticmethod
    def GetUniform4fv(uniform, count, val):
        return glUniform4fv(glGetUniformLocation(uniform), count, val)

    @staticmethod
    def GetUniform1iv(uniform, count, val):
        return glUniform1iv(glGetUniformLocation(uniform), count, val)

    @staticmethod
    def GetUniform2iv(uniform, count, val):
        return glUniform2iv(glGetUniformLocation(uniform), count, val)

    @staticmethod
    def GetUniform3iv(uniform, count, val):
        return glUniform3iv(glGetUniformLocation(uniform), count, val)

    @staticmethod
    def GetUniform4iv(uniform, count, val):
        return glUniform4iv(glGetUniformLocation(uniform), count, val)

    @staticmethod
    def GetUniform1uiv(uniform, count, val):
        return glUniform1uiv(glGetUniformLocation(uniform), count, val)

    @staticmethod
    def GetUniform2uiv(uniform, count, val):
        return glUniform2uiv(glGetUniformLocation(uniform), count, val)

    @staticmethod
    def GetUniform3uiv(uniform, count, val):
        return glUniform3uiv(glGetUniformLocation(uniform), count, val)

    @staticmethod
    def GetUniform4uiv(uniform, count, val):
        return glUniform4uiv(glGetUniformLocation(uniform), count, val)

    @staticmethod
    def GetUniformMatrix2fv(uniform, count, trans, val):
        return glUniformMatrix2fv(glGetUniformLocation(uniform), count, trans, val)

    @staticmethod
    def GetUniformMatrix3fv(uniform, count, trans, val):
        return glUniformMatrix3fv(glGetUniformLocation(uniform), count, trans, val)

    @staticmethod
    def GetUniformMatrix4fv(uniform, count, trans, val):
        return glUniformMatrix4fv(glGetUniformLocation(uniform), count, trans, val)

    @staticmethod
    def GetUniformMatrix2x3fv(uniform, count, trans, val):
        return glUniformMatrix2x3fv(glGetUniformLocation(uniform), count, trans, val)

    @staticmethod
    def GetUniformMatrix3x2fv(uniform, count, trans, val):
        return glUniformMatrix3x2fv(glGetUniformLocation(uniform), count, trans, val)

    @staticmethod
    def GetUniformMatrix2x4fv(uniform, count, trans, val):
        return glUniformMatrix2x4fv(glGetUniformLocation(uniform), count, trans, val)

    @staticmethod
    def GetUniformMatrix4x2fv(uniform, count, trans, val):
        return glUniformMatrix4x2fv(glGetUniformLocation(uniform), count, trans, val)

    @staticmethod
    def GetUniformMatrix3x4fv(uniform, count, trans, val):
        return glUniformMatrix3x4fv(glGetUniformLocation(uniform), count, trans, val)

    @staticmethod
    def GetUniformMatrix4x3fv(uniform, count, trans, val):
        return glUniformMatrix4x3fv(glGetUniformLocation(uniform), count, trans, val)

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
