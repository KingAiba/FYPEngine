import os
import simpleaudio


# sound = simpleaudio.WaveObject.from_wave_file(
# os.path.dirname(__file__) + "/../res/SoundEffects/scifi_weapon1.wav")
# sound.play()


class AudioManager:
    def __init__(self):
        self.Sounds = {}
        self.PlayObject = {}

    def LoadSound(self, path, key):
        path = self.GetPath() + path
        sound = simpleaudio.WaveObject.from_wave_file(path)
        self.Sounds[key] = sound

    def Play(self, key):
        if key in self.Sounds:
            self.Sounds[key].play()
        else:
            print("ERROR : Incorrect Key")

    def getAudioObj(self, key):
        if key in self.Sounds:
            return self.Sounds[key]
        else:
            print("ERROR : Incorrect Key")

    def LoopPlay(self, key):
        if key in self.PlayObject:
            if self.PlayObject[key].is_playing():
                pass
            else:
                del self.PlayObject[key]
                self.PlayObject[key] = self.Sounds[key].play()
        else:
            if key in self.Sounds:
                self.PlayObject[key] = self.Sounds[key].play()
            else:
                print("ERROR : Incorrect key")

    @staticmethod
    def GetPath():
        return os.path.dirname(__file__) + "/../../res"
