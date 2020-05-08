import glfw
from OpenGL.GL import *

KEY_W = glfw.KEY_W
KEY_A = glfw.KEY_A
KEY_S = glfw.KEY_S
KEY_D = glfw.KEY_D
KEY_Q = glfw.KEY_Q
KEY_E = glfw.KEY_E
KEY_ESC = glfw.KEY_ESCAPE
KEY_SPACE = glfw.KEY_SPACE
KEY_ENTER = glfw.KEY_ENTER
KEY_1 = glfw.KEY_1
KEY_2 = glfw.KEY_2
KEY_3 = glfw.KEY_3


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

    @staticmethod
    def key_string_to_glfw(keystr):

        if keystr == "A":
            return KEY_A
        elif keystr == "W":
            return KEY_W
        elif keystr == "D":
            return KEY_D
        elif keystr == "S":
            return KEY_S
        elif keystr == "Q":
            return KEY_Q
        elif keystr == "E":
            return KEY_E
        elif keystr == "ESC":
            return KEY_ESC
        elif keystr == "SPACE":
            return KEY_SPACE
        elif keystr == "ENTER":
            return KEY_ENTER
        elif keystr == "1":
            return KEY_1
        elif keystr == "2":
            return KEY_2
        elif keystr == "3":
            return KEY_3
