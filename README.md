# FYPEngine

### How to setup project

##### Requirements
	1. git bash
	3. Python 3.7 or above
	2. Pycharm

##### Setup
First we need to use **git bash** to download the remote repository to your project folder

```bash
git init
git clone https://github.com/kingstonxy/FYPEngine.git
```
After this make a new **Pycharm** project in the same folder. Now we need to configure the 
virtual enviroment for the project, we can add a new virtual enviroment by either:

 - Press the Interpreter widget at the bottom right of the editor
 - CTRL+ALT+S to go into the settings, Project > Project Interpeter > click the gear icoc > Add Interpreter

Now we need to run requirements.txt file using pip in the pycharm terminal to install the required libraries. 
```bash
pip install -r requirements.txt
```
The project should be setup now and to check if everything is working properly run the **main.py** or **main2.py** files, in the FYPEngine\Source folder, 
to start either of the sample games.