# FYPEngine

### How to setup project

##### Requirements
	1. Git Bash
	3. Python 3.7 or above
	2. Pycharm

##### Setup
First we need to use **git bash** to download the remote repository to your project folder

```bash
git init
git clone https://github.com/kingstonxy/FYPEngine.git
```
After this make a new **Pycharm** project in the same folder. Now we need to configure the 
virtual environment for the project, we can add a new virtual environment by either:

 - Press the Interpreter widget at the bottom right of the editor
 - CTRL+ALT+S to go into the settings, Project > Project Interpreter > Click the gear icon > Add Interpreter

Now we need to run requirements.txt file using pip in the pycharm terminal to install the required libraries. 
```bash
pip install -r requirements.txt
```
The project should be setup now and to check if everything is working properly run the **main.py** or **main2.py** files, in the FYPEngine\Source folder, 
to start either of the sample games.

### Making a new game
To make a game, first we need to make a small game class, similar to:
#### tutorialGame.py
```python
class Game:
    def __init__(self, width, height, keys):
        self.width = width
        self.height = height

    def InitRenderer(self):
        return

    def Update(self, dt):
        return

    def ProccessInput(self, dt):
        return

    def Render(self):
        return
```
After this import the required libraries.
```python
import glm
from OpenGL.GL import *

from Source.Renderer.windowManager import Window
from Source.Renderer.ResourseManager import Resources
from Source.Renderer.SpriteRender import SpriteRender
```
Now we need to load some textures and shader to setup the renderer. We can do this by
using the ``Resources.LoadShader(VertexShader FilePath, FragmentShader FilePath, Key)``
& ``Resources.LoadTexture(Texture FilePath,isAlpha, Key)``.

```python
def InitRenderer(self):

    Resources.LoadShader(os.path.dirname(__file__) +"/../../res/Shaders/BatchRenderVS2D.vs",
                             os.path.dirname(__file__) +"/../../res/Shaders/BatchRenderFS2D.fs", "Shader")

    Resources.LoadTexture(os.path.dirname(__file__) + "/../../res/Textures/DurrrSpaceShip.png", 1,
                              "ship")

```
To setup the renderer we need  to include the following line in ``InitRenderer``
```python
Renderer = None
class Game:
            .
            . 
            .

def InitRenderer(self):
            .
            .
            .

    Renderer = SpriteRender(self.Resource.Shaders["Shader"])
    projection = glm.ortho(0.0, self.width, self.height, 0.0, -1.0, 1.0)

    glUniformMatrix4fv(glGetUniformLocation(self.Resource.Shaders["Shader"].ID, "projection"), 1, GL_FALSE,
                        glm.value_ptr(projection))
            .
            .
    
```
We can draw objects in ``def Render(self)`` function by calling ``Renderer.DrawSprite(texture, position, size, rotate, color):``
```python
 def Render(self):
    self.Resource.Textures["ship"], glm.vec2(100, 100),
                           glm.vec2(200, 200), 0.0, glm.vec3(1.0, 1.0, 1.0)

```
Make a main function at the end of the file like:
```python

WIDTH = 800
HEIGHT = 600


NewGame = Game(WIDTH, HEIGHT)
def main():
    window = Window()

    window.CreateWindow(WIDTH, HEIGHT, "tutorial")

    NewGame.InitRenderer()

    while not window.isWindowClosed():

        deltaTime = window.GetDeltaTime()
        window.PollEvents()

        NewGame.ProccessInput(deltaTime)
        NewGame.Update(deltaTime)
        window.BackgroundColor(0.5, 0.2, 1.0, 1.0)
        NewGame.Render()
        window.SwapBuffers()

    window.End()
    return 0


main()
```
this should draw the specified object and textures.

#### tutorialGame.py

####