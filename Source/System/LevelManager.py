class LevelManager:
    def __init__(self, system):
        self.gameObjects = []
        self.player = None
        self.System = system

    def InitLevel(self):
        # self.System.InitSystems()
        pass

    def AddObject(self, newObject):
        self.gameObjects.append(newObject)

    def Remove(self, Object):
        self.gameObjects.remove(Object)

    def Update(self, dt):
        for Objects in self.gameObjects:
            if Objects.Animated:
                Objects.playAnimation(dt)
            if Objects.ObjectType is not "STATIC":
                Objects.Update(dt)

    def Draw(self):
        for Objects in self.gameObjects:
            Objects.Draw(self.System)

    def BatchDraw(self):
        for Objects in self.gameObjects:
            Objects.BatchDraw(self.System)

    def ClearLevel(self):
        self.gameObjects.clear()
