# breakout-game

An OpenGL version of the Breakout game, implemented using Python 3.8 and PyOpenGL package.

The game was made as an assignment for the Computer Graphics course at UFMG in the first term of 2020 (01/2020)

## Game Footage

YouTube link with game footage: https://youtu.be/fx-5n6SY0wI

## Instructions

### Windows

* Go to https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl

 * Download the files "PyOpenGL‑3.1.5‑cpXX‑cpXX‑win_amd64.whl" and "PyOpenGL_accelerate‑3.1.5‑cpXX‑cpXX‑win_amd64.whl", replace "XX" with your python version. Ex: 38 for Python 3.8
 
 * Install them by runing the following commands on cmd/powershell:
 
`pip install PyOpenGL-3.1.5-cpXX-cpXX-win_amd64.whl`

`pip install PyOpenGL_accelerate‑3.1.5‑cpXX‑cpXX‑win_amd64.whl`

* To play the game, run on terminal:

`python game.py`

### Ubuntu/Debian

*(Not tested)*

To install the required software/packages, run on terminal: 

`sudo apt-get install python3-pip`

`pip3 install PyOpenGL PyOpenGL_accelerate`

`sudo apt-get install freeglut3`

To play the game, run on terminal:

`python game.py`

## Implementation

The GameObj class keeps the positions left, bottom, right, top of the object and has a method that checks if there was a collision with another object passed by parameter, including in the corners or the middle. This class is used for all graphical objects in the game except text. The game walls are also of this class. The collision with the wall is calculated in another way, as the ball is "in" the walls of the game.

The bricks are stored in two matrices. One holds the color information, and the other holds the brick itself. The brick is wide enough to fill the canvas. The set of bricks walks across the screen, respecting the brick's position on the far left and far right.

The game starts on the first level, with four bricks on the screen and a row of bricks. At each level, increase two more bricks and one more row. The last level is 4, where there are 4 rows and 10 bricks each. Each level adds a color variation, which respects a hierarchy (the ball needs to hit this brick an X number of times before it is eliminated, with X depending on the color level):
green <- yellow <- orange <- red

The speed of the paddle adds to the speed of the ball. The position in which the ball hits the paddle also influences its speed (in the corners is greater than in the middle). The speed of the paddle depends on how far you are from the mouse on the screen (the farther away, the greater, to try to reach it)

The speed of the ball and bricks increases with each level. The maximum ball count also increases by 5 * (current level - 1) 



