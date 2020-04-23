import glm

class Camera2D:

    def __init__(self, screenWidth, screenHeight):
        self.position = glm.vec2(0)
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.scale = 0.0
        self.orthoMatrix = glm.ortho(0.0, self.screenWidth, 0.0, self.screenHeight)

    def setPosition(self, newPosition):
        self.position = newPosition

    def getPosition(self):
        return self.position

    def setScale(self, newScale):
        self.scale = newScale

    def getScale(self):
        return self.scale

    def getCameraMatrix(self):
        return self.orthoMatrix

    def update(self):
        cameraMatrix = glm.translate(self.orthoMatrix, glm.vec3(self.position.x, self.position.y, 0.0))
        cameraMatrix = glm.scale(cameraMatrix, glm.vec3(self.scale, self.scale, 0.0))
        return cameraMatrix



