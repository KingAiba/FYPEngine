class Animation:

    def __init__(self):
        self.state = 0
        self.speed = float(1.0)
        self.AnimationList = []
        self.accumulator = float(0.0)

    def Play(self, dt):
        self.accumulator += dt
        if self.speed < self.accumulator:
            self.state += 1
            self.accumulator = 0.0
            if self.state > len(self.AnimationList) - 1:
                self.state = 0
        return self.AnimationList[self.state]

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state

    def setSpeed(self, speed):
        self.speed = speed

    def getSpeed(self):
        return self.speed
# 8- 12
