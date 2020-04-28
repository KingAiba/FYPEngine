import glfw
from OpenGL.GL import *


class Window:
    def __init__(self):
        self.window = None
        self.LastFrame = float(0.0)
        self.dt = float(0.0)

    def CreateWindow(self, width, height, title):
        if not glfw.init():
            print("ERROR : Could not Init GLFW")
            exit()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        self.window = glfw.create_window(width, height, title, None, None)

        if not self.window:
            print("ERROR : Window Creation Failed")
            glfw.terminate()
            exit()

        glfw.make_context_current(self.window)
        glViewport(0, 0, width, height)
        glEnable(GL_CULL_FACE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        return self.window

    def GetDeltaTime(self):

        currentTime = glfw.get_time()
        self.dt = currentTime - self.LastFrame
        self.LastFrame = currentTime

        return self.dt

    def isWindowClosed(self):
        return glfw.window_should_close(self.window)

    @staticmethod
    def PollEvents():
        glfw.poll_events()

    def SwapBuffers(self):
        glfw.swap_buffers(self.window)

    @staticmethod
    def BackgroundColor(r, g, b, alpha):
        glClearColor(r, g, b, alpha)
        glClear(GL_COLOR_BUFFER_BIT)

    @staticmethod
    def End():
        glfw.terminate()
