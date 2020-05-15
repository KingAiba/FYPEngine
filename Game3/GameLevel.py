import os
import sys
import glm

sys.path.append(os.path.dirname(__file__) + "/../")
from Source.System.LevelManager import LevelManager
from Source.System.animationComponent import Animation
from Game3.GameObjects import Player
from Game3.GameObjects import Tile

playerVelocity = float(250)


class GameLevel(LevelManager):

    def __init__(self, system):
        super().__init__(system)
        self.player = None
        self.staticObjects = []

    def InitLevel(self):
        super().InitLevel()
        # load resources
        self.System.LoadTextureToResources(os.path.dirname(__file__) + "/../res/Textures/tile_spritesheet.png", 1,
                                           "TileSheet")

        # init objects
        idleAnimation = Animation()
        idleAnimation.speed = 0.25
        idleAnimation.AnimationList = [glm.vec2(1, 1), glm.vec2(2, 1), glm.vec2(3, 1), glm.vec2(4, 1)]

        walkingAnimation = Animation()
        walkingAnimation.speed = 0.20
        walkingAnimation.AnimationList = [glm.vec2(1, 2), glm.vec2(2, 2), glm.vec2(3, 2), glm.vec2(4, 2),
                                          glm.vec2(5, 2), glm.vec2(6, 2)]

        jumpAnimation = Animation()
        jumpAnimation.speed = 0.15
        jumpAnimation.AnimationList = [glm.vec2(7, 2), glm.vec2(8, 2), glm.vec2(1, 3), glm.vec2(2, 3), glm.vec2(3, 3),
                                       glm.vec2(4, 3), glm.vec2(5, 3), glm.vec2(6, 3), glm.vec2(7, 3), glm.vec2(8, 3)]

        Player1 = Player(os.path.abspath(__file__) + "/../../res/GameObjects/Player.xml")

        Player1.Animated = True
        Player1.addAnimation(idleAnimation)
        Player1.addAnimation(walkingAnimation)
        Player1.addAnimation(jumpAnimation)
        Player1.position = glm.vec2(530, 100)
        Player1.TexID = 0
        Player1.VerticalFlip = 0
        Player1.Velocity = glm.vec2(0, 0)
        self.player = Player1

        testTile = Tile()
        testTile.position = glm.vec2(500, 500)
        testTile.Size = glm.vec2(200, 200)
        testTile.Grid = glm.vec2(6, 4)
        testTile.Selected = glm.vec2(3, 2)
        testTile.TexID = 2
        testTile.Texture = "TileSheet"

        testTile2 = Tile()
        testTile2.position = glm.vec2(100, 500)
        testTile2.Size = glm.vec2(200, 200)
        testTile2.Grid = glm.vec2(6, 4)
        testTile2.Selected = glm.vec2(3, 4)
        testTile2.TexID = 2
        testTile2.Texture = "TileSheet"

        # self.AddObject(player)
        self.AddObject(Player1)
        self.staticObjects.append(testTile)
        self.staticObjects.append(testTile2)

    def Update(self, dt):
        i = 0
        print(self.player.Velocity)

        # print(self.System.GetDeltaTime())
        keys = self.System.GetInput()

        if keys[self.System.getKey("A")]:
            self.player.Velocity.x = -150
            self.player.VerticalFlip = 1
            i = 1

        if keys[self.System.getKey("D")]:
            self.player.Velocity.x = 150
            self.player.VerticalFlip = 0
            i = 1

        if keys[self.System.getKey("SPACE")]:
            self.player.jump()
            i = 2

        self.player.ChangeAnimationState(i)
        if not (keys[self.System.getKey("D")] or keys[self.System.getKey("A")]):

            self.player.Velocity.x = 0

        for Objects in self.staticObjects:
            if self.player.TileCollision(Objects):
                self.player.position.y = Objects.position.y - self.player.Size.y
                self.player.CollisionFlag = 1
                if not keys[self.System.getKey("SPACE")]:
                    self.player.JumpFlag = 0
                break
            else:
                self.player.CollisionFlag = 0


        super().Update(dt)

    def BatchDraw(self):
        for Objects in self.staticObjects:
            Objects.BatchDraw(self.System)
        super().BatchDraw()