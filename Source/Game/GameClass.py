import glm
import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from Source.Renderer.ResourseManager import ResourceManager
from Source.Renderer.ResourseManager import Resources
from Source.Renderer.SpriteRender import SpriteRender
from Source.Renderer.ParticleSystem import Generator
from Source.Game.GameLevel import GameLevel
from Source.Game.GameObject import GameObject
from Source.Game.GameObject import BallObject

Player_Size = glm.vec2(100, 20)
Player_Velocity = float(500.0)
Ball_Velocity = glm.vec2(100.0, -350.0)
Ball_Radius = 12.5


def CheckCollision(Obj1, Obj2):
    ColX = False
    ColY = False

    if ((Obj1.Position.x + Obj1.Size.x) >= Obj2.Position.x) and ((Obj2.Position.x + Obj2.Size.x) >= Obj1.Position.x):
        ColX = True
    if ((Obj1.Position.y + Obj1.Size.y) >= Obj2.Position.y) and ((Obj2.Position.y + Obj2.Size.y) >= Obj1.Position.y):
        ColY = True

    return ColX and ColY


def CheckCircleCollision(Ball, Obj):
    # find center of call
    center = glm.vec2(Ball.Position + Ball.Radius)

    # calculate halk extents
    halfExtent = glm.vec2(Obj.Size.x / 2, Obj.Size.y / 2)
    aabbCenter = glm.vec2(Obj.Position.x + halfExtent.x, Obj.Position.y + halfExtent.y)

    # get difference and clamped val
    difference = center - aabbCenter
    clamped = glm.clamp(difference, -halfExtent, halfExtent)
    closest = aabbCenter + clamped
    difference = closest - center

    if glm.length(difference) < Ball.Radius:
        Collision = (GL_TRUE, CheckDirection(difference), difference)
    else:
        Collision = (GL_FALSE, "UP", glm.vec2(0, 0))

    return Collision


def CheckDirection(target):
    compass = [glm.vec2(0.0, 1.0), glm.vec2(1.0, 0.0), glm.vec2(0.0, -1.0), glm.vec2(-1.0, 0.0)]
    direction = ["UP", "RIGHT", "DOWN", "LEFT"]

    maxVal = 0.0
    bestVal = -1
    index = 0

    for value in compass:
        dotProduct = glm.dot(glm.normalize(target), value)

        if dotProduct > maxVal:
            maxVal = dotProduct
            bestVal = index

        index = index + 1

    return direction[bestVal]


class Game:
    def __init__(self, width, height, keys):
        self.width = width
        self.height = height
        self.state = "ACTIVE"
        self.keys = keys
        self.LevelsList = []
        self.Level = 0
        self.Player = None
        self.Ball = None
        self.PGen = None
        self.Resource = None
        self.Renderer = None

    def InitRenderer(self):
        self.Resource = Resources
        # Load Shader
        self.Resource.LoadShader(os.path.dirname(__file__) + "/../../res/Shaders/VS2D.vs",
                                 os.path.dirname(__file__) + "/../../res/Shaders/FS2D.fs", "Shader")
        self.Resource.LoadShader(os.path.dirname(__file__) + "/../../res/Shaders/ParticleVS.vs",
                                 os.path.dirname(__file__) + "/../../res/Shaders/ParticleFS.fs", "ParticleShader")

        # Load Textures
        self.Resource.LoadTexture(os.path.dirname(__file__) + "/../../res/Textures/player.png", 1, "playerShip")
        self.Resource.LoadTexture(os.path.dirname(__file__) + "/../../res/Textures/block.png", 0, "block")
        self.Resource.LoadTexture(os.path.dirname(__file__) + "/../../res/Textures/block_solid.png", 0, "block_solid")
        self.Resource.LoadTexture(os.path.dirname(__file__) + "/../../res/Textures/paddle.png", 1, "paddle")
        self.Resource.LoadTexture(os.path.dirname(__file__) + "/../../res/Textures/background.jpg", 0, "background")
        self.Resource.LoadTexture(os.path.dirname(__file__) + "/../../res/Textures/bg5.jpg", 0, "background2")
        self.Resource.LoadTexture(os.path.dirname(__file__) + "/../../res/Textures/sci_fi_bg1.jpg", 0, "background3")
        self.Resource.LoadTexture(os.path.dirname(__file__) + "/../../res/Textures/ball.png", 1, "ball")
        self.Resource.LoadTexture(os.path.dirname(__file__) + "/../../res/Textures/spikedball.png", 1, "spikedball")
        self.Resource.LoadTexture(os.path.dirname(__file__) + "/../../res/Textures/glasspaddle2.png", 1, "glasspaddle")
        self.Resource.LoadTexture(os.path.dirname(__file__) + "/../../res/Textures/particle.png", 1, "particle")

        # Load Levels
        Zero = GameLevel()
        Zero.Load(os.path.dirname(__file__) + "/levels/level0.txt", self.width, self.height * 0.5)
        One = GameLevel()
        One.Load(os.path.dirname(__file__) + "/levels/level1.txt", self.width, self.height * 0.5)
        Two = GameLevel()
        Two.Load(os.path.dirname(__file__) + "/levels/level2.txt", self.width, self.height * 0.5)
        Three = GameLevel()
        Three.Load(os.path.dirname(__file__) + "/levels/level3.txt", self.width, self.height * 0.5)

        # make player object
        PlayerPos = glm.vec2(self.width / 2 - Player_Size.x / 2, self.height - Player_Size.y)
        self.Player = GameObject()
        self.Player.Position = PlayerPos
        self.Player.Size = Player_Size
        self.Player.Sprite = Resources.Textures["glasspaddle"]

        # make ball object
        BallPos = PlayerPos + glm.vec2(Player_Size.x / 2 - Ball_Radius, -Ball_Radius * 2)
        self.Ball = BallObject()
        self.Ball.Position = BallPos
        self.Ball.Radius = Ball_Radius
        self.Ball.Size = glm.vec2(Ball_Radius * 2, Ball_Radius * 2)
        self.Ball.Velocity = Ball_Velocity
        self.Ball.Sprite = Resources.Textures["spikedball"]

        self.PGen = Generator(Resources.Shaders["ParticleShader"], Resources.Textures["particle"], 500)

        self.LevelsList.append(Zero)
        self.LevelsList.append(One)
        self.LevelsList.append(Two)
        self.LevelsList.append(Three)
        print(self.LevelsList)
        self.Level = 3

        self.Renderer = SpriteRender(self.Resource.Shaders["Shader"])

        projection = glm.ortho(0.0, self.width, self.height, 0.0, -1.0, 1.0)

        glUniformMatrix4fv(glGetUniformLocation(self.Resource.Shaders["Shader"].ID, "projection"), 1, GL_FALSE,
                           glm.value_ptr(projection))
        glUniformMatrix4fv(glGetUniformLocation(self.Resource.Shaders["ParticleShader"].ID, "projection"), 1, GL_FALSE,
                           glm.value_ptr(projection))

    def Update(self, dt):
        self.Ball.Move(dt, self.width)
        self.BlockCollision()
        self.PGen.Update(dt, self.Ball, 10, glm.vec2(self.Ball.Radius / 2))
        if self.Ball.Position.y >= self.height:
            self.ResetLevel()
            self.ResetPlayer()

    def ProccessInput(self, dt):

        if self.state == "ACTIVE":
            Velocity = Player_Velocity * dt
            # print("DT : " + str(dt))
            # print("Velocity : " + str(Velocity))

            if self.keys[glfw.KEY_A]:
                if self.Player.Position.x >= 0:
                    self.Player.Position.x = self.Player.Position.x - Velocity
                    if self.Ball.Stuck:
                        self.Ball.Position.x = self.Ball.Position.x - Velocity

            if self.keys[glfw.KEY_D]:
                if self.Player.Position.x <= (self.width - self.Player.Size.x):
                    self.Player.Position.x = self.Player.Position.x + Velocity
                    if self.Ball.Stuck:
                        self.Ball.Position.x = self.Ball.Position.x + Velocity

            if self.keys[glfw.KEY_SPACE]:
                self.Ball.Stuck = GL_FALSE

    def Render(self):
        if self.state == "ACTIVE":
            self.Renderer.DrawSprite(self.Resource.Textures["background3"], glm.vec2(0, 0),
                                     glm.vec2(self.width, self.height), 0.0, glm.vec3(0.3, 0.3, 0.5))

            self.LevelsList[self.Level].Draw(self.Renderer)
            self.Player.Draw(self.Renderer)
            self.PGen.Draw()
            self.Ball.Draw(self.Renderer)

            # self.Renderer.DrawSprite(self.Resource.Textures["playerShip"], glm.vec2(0, 0), glm.vec2(200, 200), 0.0,
            # glm.vec3(0.0, 1.0, 0.0)) self.Renderer.DrawSprite(self.Resource.Textures["playerShip"], glm.vec2(600,
            # 400), glm.vec2(200, 200), 0.0, glm.vec3(0.0, 1.0, 0.0))

    def BlockCollision(self):
        for Block in self.LevelsList[self.Level].Blocks:
            if not Block.Destroyed:
                Collision = CheckCircleCollision(self.Ball, Block)

                if Collision[0]:
                    if not Block.IsSolid:
                        Block.Destroyed = GL_TRUE
                        # print(Block.Destroyed)
                    Direction = Collision[1]
                    diffVector = Collision[2]

                    if Direction == "LEFT" or Direction == "RIGHT":
                        self.Ball.Velocity.x = -self.Ball.Velocity.x
                        pen = self.Ball.Radius - abs(diffVector.x)
                        if Direction == "LEFT":
                            self.Ball.Position.x = self.Ball.Position.x + pen
                        else:
                            self.Ball.Position.x = self.Ball.Position.x - pen
                    else:
                        self.Ball.Velocity.y = -self.Ball.Velocity.y
                        pen = self.Ball.Radius - abs(diffVector.y)
                        if Direction == "UP":
                            self.Ball.Position.y = self.Ball.Position.y - pen
                        else:
                            self.Ball.Position.y = self.Ball.Position.y + pen

        Collision = CheckCircleCollision(self.Ball, self.Player)

        if not self.Ball.Stuck and Collision[0]:
            # check if player hits ball
            center = self.Player.Position.x + self.Player.Size.x / 2
            distance = (self.Ball.Position.x + self.Ball.Radius) - center
            disPercent = distance / (self.Player.Size.x / 2)

            strength = float(2.0)
            OldVel = self.Ball.Velocity
            self.Ball.Velocity.x = Ball_Velocity.x * disPercent * strength

            # self.Ball.Velocity.y = -self.Ball.Velocity.y
            self.Ball.Velocity.y = -1 * abs(self.Ball.Velocity.y)
            self.Ball.Velocity = glm.normalize(self.Ball.Velocity) * glm.length(OldVel)
            # print(self.Ball.Velocity)

    def ResetLevel(self):
        if self.Level == 0:
            self.LevelsList[0].Load(os.path.dirname(__file__) + "/levels/level0.txt", self.width, self.height * 0.5)
        elif self.Level == 1:
            self.LevelsList[1].Load(os.path.dirname(__file__) + "/levels/level1.txt", self.width, self.height * 0.5)
        elif self.Level == 2:
            self.LevelsList[2].Load(os.path.dirname(__file__) + "/levels/level2.txt", self.width, self.height * 0.5)
        elif self.Level == 3:
            self.LevelsList[3].Load(os.path.dirname(__file__) + "/levels/level3.txt", self.width, self.height * 0.5)

    def ResetPlayer(self):
        self.Player.Size = Player_Size
        PlayerPos = glm.vec2(self.width / 2 - Player_Size.x / 2, self.height - Player_Size.y)
        self.Player.Position = PlayerPos
        self.Ball.Reset(PlayerPos + glm.vec2(Player_Size.x / 2 - Ball_Radius, -Ball_Radius * 2), Ball_Velocity)
