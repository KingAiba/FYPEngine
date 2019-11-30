import numpy

import glfw

from Source.Renderer.Shader import Shader

from Source.Renderer.Renderer import Renderer

from PIL import Image

from OpenGL.GL import *

from OpenGL.GLUT import *

from PIL import Image

import os

VSFILEPATH = os.path.dirname(__file__) + "/../res/Shaders/VertexShader.vs"
FSFILEPATH = os.path.dirname(__file__) + "/../res/Shaders/FragmentShader.fs"
IMAGEPATH = os.path.dirname(__file__) + "/../res/Textures/player.png"


# img = Image.open(FILEPATH)
#
# width, height = img.size
#
# img1 = img.convert('RGBA')
# img2 = img1.tobytes("PNG")
# img1.show()
# print(img2)
# print("\n")
# print(width, height)


def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)


def main():
    if not glfw.init():
        return 0

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE);

    window = glfw.create_window(800, 600, "OPENGL_TextureExample", None, None)

    if not window:
        print("Window Creation Failed")
        glfw.terminate()
        return 0

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    myShader = Shader(VSFILEPATH, FSFILEPATH)
    myRenderer = Renderer("myRenderer")
    #                       position      color          tex coords
    vertices = numpy.array([0.5, 0.5, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0,
                            0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0,
                            -0.5, 0.5, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
                            -0.5, -0.5, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0], dtype="f")
    myShader.Compile()

    VBO = GLuint(0)
    VAO = GLuint(0)
    VAO = glGenVertexArrays(1)
    VBO = myRenderer.GenBuffer(1)

    glBindVertexArray(VAO)
    myRenderer.BindBuffer(GL_ARRAY_BUFFER, VBO)
    myRenderer.BufferData(GL_ARRAY_BUFFER, 4 * (numpy.size(vertices)), vertices, GL_STATIC_DRAW)

    # Get vertex position
    # position = myRenderer.GetAttribLocation(myShader.ID, "aPos")
    myRenderer.VertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
    myRenderer.EnableVertexArribArray(0)

    # get color
    # Color = myRenderer.GetAttribLocation(myShader.ID, "aColor")
    myRenderer.VertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
    myRenderer.EnableVertexArribArray(1)

    # get tex coords
    # TexCoords = myRenderer.GetAttribLocation(myShader.ID, "aTexCoord")
    myRenderer.VertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))
    myRenderer.EnableVertexArribArray(2)

    # load and create Texture
    Texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, Texture)

    # set texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    # texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    # load image
    ImgSource = Image.open(IMAGEPATH)
    if not ImgSource:
        print("IMAGE NOT FOUND")
        return 0
    imgWidth, imgHeight = ImgSource.size

    ImgSource = ImgSource.convert("RGB")
    ImgArray = ImgSource.tobytes()
    print(ImgArray)
    if not ImgArray:
        print("ERROR CONVERTING IMAGE tobytes()")
        return 0
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, imgWidth, imgHeight, 0, GL_RGB, GL_UNSIGNED_BYTE, ImgArray)
    glGenerateMipmap(GL_TEXTURE_2D)

    myShader.UseProgram()
    glUniform1i(glGetUniformLocation(myShader.ID, "Texture"), 0)

    while not glfw.window_should_close(window):
        myRenderer.ClearColor(0.2, 0.2, 0.4, 1.0)
        myRenderer.Clear()

        glDrawArrays(GL_TRIANGLES, 0, 3)
        glDrawArrays(GL_TRIANGLES, 1, 3)

        glfw.poll_events()
        glfw.swap_buffers(window)

    glfw.terminate()
    return 0


main()
