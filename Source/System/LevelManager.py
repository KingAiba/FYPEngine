
class LevelManager:
    def __init__(self, system):
        self.gameObjects = []
        self.System = system

    def InitLevel(self):
        self.System.InitSystems()

    def AddObject(self, newObject):
        self.gameObjects.append(newObject)

    def Remove(self, Object):
        self.gameObjects.remove(Object)

    def Update(self):
        for Objects in self.gameObjects:
            Objects.Update()

    def Draw(self):
        for Objects in self.gameObjects:
            Objects.Draw(self.System)

    def ClearLevel(self):
        self.gameObjects.clear()
