import glfw
import glm
import os

from OpenGL.GL import *
from .GameScene import *
from .GameObjects import *
from Source.Renderer.ParticleSystem import Generator
from Source.Renderer.ResourseManager import Resources
from Source.Renderer.SpriteRender import SpriteRender

Player_Velocity = float(550.0)
Player_Size = glm.vec2(125, 125)


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


class Game2:
    def __init__(self, width, height, keys):
        self.width = width
        self.height = height
        self.state = "ACTIVE"
        self.keys = keys
        self.LevelList = []
        self.CurrLevel = 0
        self.CurrLevel = 1

        self.Player = None
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
        self.Resource.LoadTexture(os.path.dirname(__file__) + "/../../res/Textures/cartoonship red.png", 1, "RedShip")
        self.Resource.LoadTexture(os.path.dirname(__file__) + "/../../res/Textures/DurrrSpaceShip.png", 1,
                                  "PlayerShip2")
        self.Resource.LoadTexture(os.path.dirname(__file__) + "/../../res/Textures/boss2.png", 1, "boss")

        self.Renderer = SpriteRender(self.Resource.Shaders["Shader"])

        projection = glm.ortho(0.0, self.width, self.height, 0.0, -1.0, 1.0)

        glUniformMatrix4fv(glGetUniformLocation(self.Resource.Shaders["Shader"].ID, "projection"), 1, GL_FALSE,
                           glm.value_ptr(projection))

        self.Player = Player()

        self.Player = Player()

        self.Player.Position = glm.vec2(self.width / 2 - Player_Size.x / 2, self.height / 2 - Player_Size.x / 2)
        self.Player.Size = Player_Size
        self.Player.Health = 3
        self.Player.Sprite = Resources.Textures["PlayerShip2"]

        self.LevelList.append(Scene(Resources.Textures["background2"], 15, 15, self.width,
                                    self.height))

        self.LevelList.append(Scene(Resources.Textures["background2"], 10, 10, self.width,
                                    self.height))
        self.LevelList.append(Scene(Resources.Textures["background2"], 50, 10, self.width,

                                    self.height))
        # glUniformMatrix4fv(glGetUniformLocation(self.Resource.Shaders["ParticleShader"].ID, "projection"), 1,
        # GL_FALSE, glm.value_ptr(projection))

    def Update(self, dt):

        self.LevelList[self.CurrLevel].UpdateScene(1, dt)

        # print(1/dt)
        self.LevelList[self.CurrLevel].UpdateScene(2, dt)

        self.Player.UpdateProjectile(dt)
        self.DoCollision()
        self.CheckLoss()

    def ProccessInput(self, dt):

        if self.state == "ACTIVE":
            self.Player.Timer = self.Player.Timer + dt
            Velocity = Player_Velocity * dt

            if self.keys[glfw.KEY_S]:
                if self.Player.Position.y <= (self.height - self.Player.Size.y):
                    self.Player.Position.y = self.Player.Position.y + Velocity

            if self.keys[glfw.KEY_W]:
                if self.Player.Position.y >= 0:
                    self.Player.Position.y = self.Player.Position.y - Velocity

            if self.keys[glfw.KEY_A]:
                if self.Player.Position.x >= 0:
                    self.Player.Position.x = self.Player.Position.x - Velocity

            if self.keys[glfw.KEY_D]:
                if self.Player.Position.x <= (self.width - self.Player.Size.x):
                    self.Player.Position.x = self.Player.Position.x + Velocity

            if self.keys[glfw.KEY_SPACE]:
                self.Player.MakeProjectile(Resources.Textures["ball"], dt)

    def Render(self):
        self.LevelList[self.CurrLevel].StartScene(self.Renderer, glm.vec3(0.6, 0.6, 1.0))
        self.LevelList[self.CurrLevel].DrawShips(self.Renderer)
        self.Player.DrawProjectiles(self.Renderer)
        self.Player.Draw(self.Renderer)

    def DoCollision(self):
        ShipIndex = 0
        for ship in self.LevelList[self.CurrLevel].Curr:
            ProjectileIndex = 0
            for pro in self.Player.ProjectileList:
                Collision = CheckCollision(pro, ship)
                if Collision:
                    self.Player.DestroyProjectile(ProjectileIndex)
                    ship.Health = ship.Health - 1
                    ship.Color.x = ship.Color.x + 0.2
                ProjectileIndex = ProjectileIndex + 1

            Collision = CheckCollision(self.Player, ship)
            if Collision:
                ship.Health = ship.Health - 1
                ship.Color.x = ship.Color.x + 0.2
            ShipIndex = ShipIndex + 1

    def CheckLoss(self):
        ShipIndex = 0
        for ship in self.LevelList[self.CurrLevel].Curr:
            if ship.Position.y >= (self.height + 50):
                self.Player.Health = self.Player.Health - 1
                self.LevelList[self.CurrLevel].DelShip(ShipIndex)
            ShipIndex = ShipIndex + 1
        if self.Player.Health <= 0:
            print("GAME OVER")
