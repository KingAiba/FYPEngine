import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *

from Game2.GameClass import Game2

WIDTH = 1000
HEIGHT = 800
Keys = [GL_FALSE] * 1024

NewGame = Game2(WIDTH, HEIGHT, Keys)


def key_callback(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, GL_TRUE)

    if 0 <= key < 1024:
        # print(key)
        if action == glfw.PRESS:
            NewGame.keys[key] = GL_TRUE
        elif action == glfw.RELEASE:
            NewGame.keys[key] = GL_FALSE


def main():
    if not glfw.init():
        print("ERROR : Could not Init GLFW")
        return 0
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(WIDTH, HEIGHT, "GAME", None, None)

    if not window:
        print("ERROR : Window Creation Failed")
        glfw.terminate()
        return 0

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    glViewport(0, 0, WIDTH, HEIGHT)
    glEnable(GL_CULL_FACE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    NewGame.InitRenderer()
    NewGame.state = "ACTIVE"

    deltaTime = float(0.0)
    LastFrame = float(0.0)

    while not glfw.window_should_close(window):
        currentFrame = glfw.get_time()
        deltaTime = currentFrame - LastFrame
        LastFrame = currentFrame

        glfw.poll_events()

        NewGame.ProccessInput(deltaTime)
        NewGame.Update(deltaTime)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        NewGame.Render()
        glfw.swap_buffers(window)

    glfw.terminate()
    return 0


main()
