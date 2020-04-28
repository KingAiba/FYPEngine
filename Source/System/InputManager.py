import glfw
from OpenGL.GL import *


class InputManager:

    def __init__(self):
        self.Keys = [False] * 1024

    def key_callback(self, window, key, scancode, action, mode):

        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, GL_TRUE)

        if 0 <= key < 1024:
            # print(key)
            if action == glfw.PRESS:
                self.Keys[key] = True
            elif action == glfw.RELEASE:
                self.Keys[key] = False

    def SetCallback(self, window):
        glfw.set_key_callback(window, self.key_callback)

    def getKeys(self):
        return self.Keys
