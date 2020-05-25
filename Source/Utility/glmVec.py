import glm


# utility functions to get glm vector objects, used to abstract glm
def GetVec1(x):
    return glm.vec1(x)


def GetVec2(x, y):
    return glm.vec2(x, y)


def GetVec3(x, y, z):
    return glm.vec3(x, y, z)


def GetVec4(x, y, z, w):
    return glm.vec4(x, y, z, w)


def normalize(x):
    return glm.normalize(x)


def glmLength(x):
    return glm.length(x)
