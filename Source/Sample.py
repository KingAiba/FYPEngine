import glfw
from GameSample.gameClass import Game
from OpenGL.GL import *


keys = [GL_FALSE] * 1024
width = 800
height = 600
game_1 = Game(width, height, keys)


def key_callback(window, key, scancode, action, mode):
    # detect which key is pressed
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, GL_TRUE)

    if 0 <= key < 1024:
        # print(key)
        if action == glfw.PRESS:
            game_1.keys[key] = GL_TRUE
        elif action == glfw.RELEASE:
            game_1.keys[key] = GL_FALSE


def main(width, height, keys):
    if not glfw.init():
        return 1

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)  # set major version
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)  # set minor version
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(width, height, "Test Window", None, None)  # create window

    if not window:
        glfw.terminate()  # terminate library
        return "get some window"

    glfw.make_context_current(window)

    glViewport(0, 0, width, height)

    glfw.set_key_callback(window, key_callback)

    glEnable(GL_CULL_FACE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    game_1.initial_renderer()

    dt = 0.0  # delta time == 1/timeframe
    last_frame = 0.0

    while not glfw.window_should_close(window):
        cur_frame = glfw.get_time()  # time since window on pc
        dt = cur_frame - last_frame
        last_frame = cur_frame
        glfw.poll_events()  # input processing which key is pressed
        game_1.processInput(dt)  # game input
        game_1.update(dt)  # movement and check the collision with resolution
        glClearColor(0.2, 0.2, 0.6, 0.5)  # background color of window
        glClear(GL_COLOR_BUFFER_BIT)  # color buffer
        game_1.render()  # draw game
        glfw.swap_buffers(window)  # current buffer and drawing buffer and switch them

    glfw.terminate()
    return 0


main(width, height, keys)
