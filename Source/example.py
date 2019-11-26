import ctypes

import pyrr

import numpy

import glfw

import OpenGL.GL.shaders

from OpenGL.GL import *

from OpenGL.GLUT import *

translate_loc = None
translate = None


def translationMAT(x, y, z):
    tMat = numpy.array([[1.0, 0.0, 0.0, x],
                        [0.0, 1.0, 0.0, y],
                        [0.0, 0.0, 1.0, z],
                        [0.0, 0.0, 0.0, 1.0]], dtype="f")
    return tMat


def identityMAT():
    identity = numpy.array([[1.0, 0.0, 0.0, 0.0],
                            [0.0, 1.0, 0.0, 0.0],
                            [0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 0.0, 1.0]], dtype="f")
    return identity


def cursorPositionCallback(window, xPos, yPos):
    print("XPos:" + str(xPos) + " YPos:" + str(yPos))
    # glTranslatef()


def cursorEnterCallback(window, entered):
    if entered:
        IS_ENTERED = True
        print("ENTERED")
    else:
        IS_ENTERED = False
        print("LEFT")


def mouseButtonCallback(window, button, action, mods):
    global translate
    if button == (glfw.MOUSE_BUTTON_RIGHT) & (action == glfw.PRESS):


        translate = pyrr.Matrix44.from_translation((-0.2, -0.2, 0), dtype="f")

        glUniformMatrix4fv(translate_loc, 1, GL_FALSE, translate)
        print("Right Pressed")
    if button == (glfw.MOUSE_BUTTON_RIGHT) & (action == glfw.RELEASE):
        print("Right Released")
    if button == (glfw.MOUSE_BUTTON_LEFT) & (action == glfw.PRESS):


        translate = pyrr.Matrix44.from_translation((0.2, 0.2, 0), dtype="f")

        glUniformMatrix4fv(translate_loc, 1, GL_FALSE, translate)
        print("Left Pressed")
    if button == (glfw.MOUSE_BUTTON_LEFT) & (action == glfw.RELEASE):
        print("Left Released")


def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)


def processInput(window):
    glfw.set_cursor_pos_callback(window, cursorPositionCallback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
    glfw.set_cursor_enter_callback(window, cursorEnterCallback)
    glfw.set_mouse_button_callback(window, mouseButtonCallback)


def main():
    # Initialize glfw
    if not glfw.init():
        return
    # window creation create_window(width, height, monitor, shared)
    width = 800
    height = 600
    window = glfw.create_window(width, height, "OpenGLProj", None, None)

    # check if window is created
    if not window:
        # not created, program terminated
        glfw.terminate()
        return

    # openGL context to draw in window
    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    triangle = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
                0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
                0.0, 0.5, 0.0, 0.0, 0.0, 1.0]

    vertex_shader_source = """
            #version 330
            in vec3 position;
            in vec3 color;
            uniform mat4 scale;
            uniform mat4 rotate;
            uniform mat4 translate;
            out vec3 newColor;
            void main()
            {
                gl_Position = translate * rotate * scale * vec4(position, 1.0f);
                newColor = color;
            }
            """
    fragment_shader_source = """
            #version 330
            in vec3 newColor;
            out vec4 outColor;
            void main()
            {
                outColor = vec4(newColor, 1.0f);
            }
            """
    # Compile Vertex Shader
    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader_source, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(fragment_shader_source,
                                                                              GL_FRAGMENT_SHADER))

    vbo = GLuint(0)
    glGenBuffers(1, vbo)

    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, 72, (GLfloat * len(triangle))(*triangle), GL_STATIC_DRAW)

    # positions
    position = glGetAttribLocation(shader, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    # colors
    color = glGetAttribLocation(shader, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    glUseProgram(shader)

    global translate
    global translate_loc

    scale_loc = glGetUniformLocation(shader, 'scale')
    rotate_loc = glGetUniformLocation(shader, 'rotate')
    translate_loc = glGetUniformLocation(shader, 'translate')

    scale = identityMAT();
    rot_y = identityMAT();
    translate = identityMAT();

    glUniformMatrix4fv(scale_loc, 1, GL_FALSE, scale)
    glUniformMatrix4fv(rotate_loc, 1, GL_FALSE, rot_y)
    glUniformMatrix4fv(translate_loc, 1, GL_FALSE, translate)

    # c_translate = (GLfloat * len(translate))(*translate)
    # print(translate)

    while not glfw.window_should_close(window):
        # glfw.get_cursor_pos(window)
        # input processing
        processInput(window)

        # render
        glClearColor(0.2, 0.3, 0.4, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        # glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, 0)

        # transfrom

        # poll and swap buffers
        glfw.poll_events()
        glfw.swap_buffers(window)

    glfw.terminate()
    return 0


if __name__ == "__main__":
    main()
