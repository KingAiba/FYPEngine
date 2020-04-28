import numpy

import glfw

import glm

from Source.Renderer.Shader import Shader

from Source.Renderer.Renderer import Renderer

from OpenGL.GL import *

from OpenGL.GLUT import *

from PIL import Image

import os


class Player:
    def __init__(self, x, y, tran):
        self.x = x
        self.y = y
        self.tran = tran


# get paths
VSFILEPATH = os.path.dirname(__file__) + "/../res/Shaders/VertexShader.vs"
FSFILEPATH = os.path.dirname(__file__) + "/../res/Shaders/FragmentShader.fs"
IMAGEPATH = os.path.dirname(__file__) + "/../res/Textures/player.png"
# init shader and renderer
myShader = Shader(VSFILEPATH, FSFILEPATH)
myRenderer = Renderer("myRenderer")
myPlayer = Player(0.0, 0.0, glm.mat4(1))


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


def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_UP and action == glfw.PRESS:
        myPlayer.tran = glm.translate(myPlayer.tran, glm.fvec3(myPlayer.x, myPlayer.y + 0.1, 0.0))
        translate_loc = glGetUniformLocation(myShader.ID, 'translate')
        glUniformMatrix4fv(translate_loc, 1, GL_FALSE, glm.value_ptr(myPlayer.tran))
        print("UP KEY PRESSED")
    if key == glfw.KEY_DOWN and action == glfw.PRESS:
        myPlayer.tran = glm.translate(myPlayer.tran, glm.fvec3(myPlayer.x, myPlayer.y - 0.1, 0.0))
        translate_loc = glGetUniformLocation(myShader.ID, 'translate')
        glUniformMatrix4fv(translate_loc, 1, GL_FALSE, glm.value_ptr(myPlayer.tran))
        print("DOWN KEY PRESSED")
    if key == glfw.KEY_RIGHT and action == glfw.PRESS:
        myPlayer.tran = glm.translate(myPlayer.tran, glm.fvec3(myPlayer.x + 0.1, myPlayer.y, 0.0))
        translate_loc = glGetUniformLocation(myShader.ID, 'translate')
        glUniformMatrix4fv(translate_loc, 1, GL_FALSE, glm.value_ptr(myPlayer.tran))
        print("RIGHT KEY PRESSED")
    if key == glfw.KEY_LEFT and action == glfw.PRESS:
        myPlayer.tran = glm.translate(myPlayer.tran, glm.fvec3(myPlayer.x - 0.1, myPlayer.y, 0.0))
        translate_loc = glGetUniformLocation(myShader.ID, 'translate')
        glUniformMatrix4fv(translate_loc, 1, GL_FALSE, glm.value_ptr(myPlayer.tran))
        print("LEFT KEY PRESSED")


def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)


def main():
    if not glfw.init():
        return 0

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE);

    screenWidth = 800
    screenHeight = 600

    window = glfw.create_window(screenWidth, screenHeight, "OPENGL_TextureExample", None, None)

    if not window:
        print("Window Creation Failed")
        glfw.terminate()
        return 0

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    glfw.set_key_callback(window, key_callback)

    #                       position      color          tex coords
    vertices = numpy.array([0.5, 0.5, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
                            0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0,
                            -0.5, 0.5, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
                            0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0,
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
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    #glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # load image
    ImgSource = Image.open(IMAGEPATH)
    if not ImgSource:
        print("IMAGE NOT FOUND")
        return 0
    imgWidth, imgHeight = ImgSource.size

    ImgSource = ImgSource.convert("RGBA")
    ImgArray = ImgSource.tobytes()
    print(ImgArray)
    if not ImgArray:
        print("ERROR CONVERTING IMAGE tobytes()")
        return 0


    # glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, imgWidth, imgHeight, 0, GL_RGBA, GL_UNSIGNED_BYTE, ImgArray)
    # glGenerateMipmap(GL_TEXTURE_2D)

    myShader.UseProgram()

    scale_loc = glGetUniformLocation(myShader.ID, 'scale')
    rotate_loc = glGetUniformLocation(myShader.ID, 'rotate')
    translate_loc = glGetUniformLocation(myShader.ID, 'translate')
    #model_loc = glGetUniformLocation(myShader.ID, 'model')
    #view_loc = glGetUniformLocation(myShader.ID, 'view')
    # projection_loc = glGetUniformLocation(myShader.ID, 'P')

    projection = glm.mat4(1)
    # using glm for view frustum // perspective(fov, aspect ratio, near clipping plane, far clipping plane)
    # projection = glm.perspective(45.0, screenWidth / screenHeight, 0.1, 1000.0)

    # projection = glm.ortho(0.0, 800.0, 0.0, 600.0, 0.1, 1000.0)


    scale = glm.fmat4(1)
    rot = glm.fmat4(1)
    translate = glm.fmat4(1)

    glUniformMatrix4fv(scale_loc, 1, GL_FALSE, glm.value_ptr(scale))
    glUniformMatrix4fv(rotate_loc, 1, GL_FALSE, glm.value_ptr(rot))
    glUniformMatrix4fv(translate_loc, 1, GL_FALSE, glm.value_ptr(translate))
    #glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(model))
    #glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view))
    # glUniformMatrix4fv(projection_loc, 1, GL_FALSE, glm.value_ptr(projection))

    glUniform1i(glGetUniformLocation(myShader.ID, "Texture"), 0)

    while not glfw.window_should_close(window):
        myRenderer.ClearColor(0.2, 0.2, 0.4, 1.0)
        myRenderer.Clear()

        glDrawArrays(GL_TRIANGLES, 0, 6)


        glfw.poll_events()
        glfw.swap_buffers(window)

    glfw.terminate()
    return 0


main()
