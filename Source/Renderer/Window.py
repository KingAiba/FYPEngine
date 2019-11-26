import glfw
import os
from xml.dom import minidom

FILEPATH = os.path.dirname(__file__) + "/../../res/Config/System.xml"


class Window:

    def __init__(self):

        if not glfw.init():
            print("ERROR: GLFW NOT INIT")
            return -1

        self.header = None
        self.width = None
        self.height = None
        self.monitor = None
        self.share = None


        myConfig = minidom.parse(FILEPATH)
        options = myConfig.getElementsByTagName('window')
        for elements in options:

            if elements.attributes['name'].value == 'header':
                self.header = (elements.firstChild.data)

            elif elements.attributes['name'].value == 'width':
                self.width = int(elements.firstChild.data)

            elif elements.attributes['name'].value == 'height':
                self.height = int(elements.firstChild.data)

            elif elements.attributes['name'].value == 'monitor':
                if elements.firstChild.data == 'None':
                    self.monitor = None

                else:
                    self.monitor = elements.firstChild.data

            elif elements.attributes['name'].value == 'share':
                if elements.firstChild.data == 'None':
                    self.share = None

                else:
                    self.share = elements.firstChild.data





mySetting = Window()
window = glfw.create_window(mySetting.width, mySetting.height, mySetting.header, mySetting.monitor, mySetting.share)
glfw.make_context_current(window)
while not glfw.window_should_close(window):
    glfw.poll_events()
    glfw.swap_buffers(window)
glfw.terminate()





