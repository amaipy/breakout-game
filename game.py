from GameObj import CORNER, GameObj

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys 

from random import seed, randint

import math

XSPEED = 6
YSPEED = -6
DELTA = 6

P_SPEED = 50

BRICK_H = 50
BRICK_W = 40

MOUSE_X = 0

MAX_LEVEL = 4
CURR_LEVEL = 1
BASE_SPEED = 4
BRICKS_SPEED = 4
CURR_BRICK_SPEED = 0
LAST_SCORE = 0

QTD_BRICKS_LVL = 4

COLL_LEFT = 1
COLL_RIGHT = 2
COLL_TOP = 3
COLL_BOTTOM = 4

BALLS_COUNT = 10
GAME_OVER = False
GAME_WIN = False
LAST_SPEED = 0
DEBUG = False
PAUSE = True 
SCORE = 0

redisplay_interval = int(1000/60)

WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 1000

bricks = []
bricks_list = []

def init_bricks():
    global bricks, bricks_list
    bricks = [[0 for _ in range(CURR_LEVEL)] for __ in range(QTD_BRICKS_LVL)] 
    bricks_list = [[None for _ in range(CURR_LEVEL)] for __ in range(QTD_BRICKS_LVL)]

    for i in range (QTD_BRICKS_LVL):
        for j in range (CURR_LEVEL):
            bricks[i][j] = randint(1, CURR_LEVEL)
            bricks_list[i][j] = GameObj()

init_bricks()

ball = GameObj((WINDOW_WIDTH/2)-10, (WINDOW_WIDTH/2)+10, (WINDOW_HEIGHT/2) + 20, WINDOW_HEIGHT/2)  
wall = GameObj()
player_1 = GameObj((WINDOW_WIDTH/2)-40, (WINDOW_WIDTH/2)+40, 220, 200)

def draw_speed(speed):
    drawText("SPEED: ", 10, 110)
    speed = float("{:.2f}".format(speed))
    speed_obj = GameObj(120, 120 + (10 * speed), 130, 110)
    draw_rect(speed_obj)

def draw_circle(ball):
    radius = int((ball.right - ball.left) / 2)
    x = ball.right - radius
    y = ball.top - int((ball.top - ball.bottom) / 2)
    triangleAmount = 20
    two_pi = 2 * math.pi
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for i in range (triangleAmount + 1):
        glVertex2f(x + (radius * math.cos(i *  two_pi / triangleAmount)), y + (radius * math.sin(i * two_pi / triangleAmount)))
    glEnd()

def draw_rect(rect):
    glBegin(GL_QUADS)
    glVertex2f(rect.left, rect.bottom)
    glVertex2f(rect.right, rect.bottom)
    glVertex2f(rect.right, rect.top)
    glVertex2f(rect.left, rect.top)
    glEnd()
        
def timer(v):
    global CURR_BRICK_SPEED, BRICKS_SPEED, LAST_SPEED, XSPEED, YSPEED, BALLS_COUNT, GAME_OVER, LAST_SCORE, SCORE, CURR_LEVEL, DELTA, GAME_WIN, QTD_BRICKS_LVL, ball, PAUSE
    if not GAME_WIN:
        if not GAME_OVER:
            if not PAUSE:
                ball.left += XSPEED
                ball.right += XSPEED
                ball.bottom += YSPEED
                ball.top += YSPEED

                direction = (MOUSE_X - player_1.right) * (1 / player_1.right)
                
                LAST_SPEED = P_SPEED * direction

                player_1.right = player_1.right + LAST_SPEED

                if player_1.right > wall.right:
                    player_1.right = wall.right
                
                elif player_1.right - 80 < wall.left:
                    player_1.right = wall.left + 80
                
                player_1.left = player_1.right - 80  

                collision_player = ball.test_collision(player_1)

                if collision_ball_wall(ball, wall) == COLL_RIGHT:
                    XSPEED = -DELTA
                if collision_ball_wall(ball, wall) == COLL_LEFT:
                    XSPEED = DELTA
                if collision_ball_wall(ball, wall) == COLL_TOP:
                    YSPEED = -DELTA

                if collision_ball_wall(ball, wall) == COLL_BOTTOM:
                    BALLS_COUNT -= 1
                    ball.bottom = WINDOW_HEIGHT/2 - 10
                    YSPEED = -DELTA
                    ball.top = 20 + ball.bottom
                    if BALLS_COUNT == 0:
                        GAME_OVER = True
                elif collision_player[0]:
                    inc = 0.01
                    if collision_player[1] == CORNER:
                        inc += 0.05
                    YSPEED = DELTA + abs(LAST_SPEED * 0.2) + abs(DELTA * inc)
                
                aux_left_brick = QTD_BRICKS_LVL
                aux_right_brick = 0

                for i in range (QTD_BRICKS_LVL):
                    for j in range(CURR_LEVEL):
                        if bricks[i][j] != 0:
                            if i < aux_left_brick:
                                aux_left_brick = i
                            if i > aux_right_brick:
                                aux_right_brick = i
                            if ball.test_collision(bricks_list[i][j])[0]:
                                XSPEED = -XSPEED
                                YSPEED = -YSPEED
                                bricks[i][j] -= 1
                                if bricks[i][j] == 0:
                                    SCORE += 1
                                break
                
                if SCORE == (QTD_BRICKS_LVL * CURR_LEVEL) + LAST_SCORE:
                    CURR_LEVEL += 1 
                    LAST_SCORE = SCORE
                    if CURR_LEVEL > MAX_LEVEL:
                        GAME_WIN = True
                    else:
                        QTD_BRICKS_LVL += 2
                        init_bricks()
                        BRICKS_SPEED = abs(BRICKS_SPEED)
                        BRICKS_SPEED += BASE_SPEED * (CURR_LEVEL/10)
                        BALLS_COUNT += 5 * (CURR_LEVEL-1)
                        DELTA += 1
                        PAUSE = True
                        ball = GameObj((WINDOW_WIDTH/2)-10, (WINDOW_WIDTH/2)+10, (WINDOW_HEIGHT/2) + 20, WINDOW_HEIGHT/2)  
                        CURR_BRICK_SPEED = 0
                        YSPEED = -DELTA 
    
                CURR_BRICK_SPEED += BRICKS_SPEED
                
                if (CURR_BRICK_SPEED + 10 + (aux_left_brick * BRICK_W)) < -100 or ((aux_right_brick * BRICK_W) + 10 + CURR_BRICK_SPEED > WINDOW_WIDTH + 100):
                    BRICKS_SPEED = -BRICKS_SPEED

    
    glutTimerFunc(redisplay_interval, timer, 1)

def drawText(str, x, y, small=False):
    glPushMatrix()
    glTranslatef(x, y, 0)
    if small:
        glScalef(0.15, 0.15, 1)
    else:
        glScalef(0.2, 0.2, 1)
    for ch in str:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ctypes.c_int(ord(ch)))
    glPopMatrix()                                         

def stop():
    sys.exit()

def collision_ball_wall(ball, wall):
    if ball.right >= wall.right:
        return COLL_RIGHT
    if ball.left <= wall.left:
        return COLL_LEFT
    if ball.top >= wall.top:
        return COLL_TOP
    if ball.bottom <= wall.bottom:
        return COLL_BOTTOM
    else: 
        return 0 

def keyboard(key, x, y):
    global SCORE, XSPEED, YSPEED, BALLS_COUNT, GAME_OVER, ball, player_1, PAUSE, bricks, bricks_list, GAME_WIN, CURR_LEVEL, LAST_SCORE, QTD_BRICKS_LVL, CURR_BRICK_SPEED, DELTA
    key = (key.decode()).lower()
    if key == 'q':
        stop()
    if key == 'r':
        ball = GameObj((WINDOW_WIDTH/2)-10, (WINDOW_WIDTH/2)+10, (WINDOW_HEIGHT/2) + 20, WINDOW_HEIGHT/2)   
        player_1 = GameObj((WINDOW_WIDTH/2)-40, (WINDOW_WIDTH/2)+40, 220, 200)
        BALLS_COUNT = 10
        GAME_WIN = False
        GAME_OVER = False
        LAST_SCORE = 0
        QTD_BRICKS_LVL = 4
        PAUSE = True
        CURR_LEVEL = 1
        SCORE = 0
        CURR_BRICK_SPEED = 0
        DELTA = 6
        YSPEED = -DELTA
        init_bricks()

def onMouseButton(button, state, x, y):
    global PAUSE, DEBUG
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        PAUSE = not PAUSE
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if not DEBUG:
            DEBUG = PAUSE = True
        else:
            PAUSE = False
            
def mouse (x, y):
    global MOUSE_X
    MOUSE_X = x

def reshape(w, h):
    global WINDOW_WIDTH, WINDOW_HEIGHT
    WINDOW_WIDTH = w
    WINDOW_HEIGHT = h

    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, w, 0.0, h, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def render():
    global BRICK_W
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    if not GAME_WIN:
        if not GAME_OVER:
            
            drawText("TRIES: {0}".format(BALLS_COUNT), 10, 40)
            drawText("SCORE: {0}".format(SCORE), 10, 80)

            wall.left = 0
            wall.bottom = player_1.bottom
            wall.right = WINDOW_WIDTH 
            wall.top = WINDOW_HEIGHT

            BRICK_W = int(WINDOW_WIDTH/QTD_BRICKS_LVL)
            
            for i in range (QTD_BRICKS_LVL):
                for j in range(CURR_LEVEL):
                    if bricks[i][j] != 0:
                        bricks_list[i][j].left = BRICK_W * i + (10) + CURR_BRICK_SPEED
                        bricks_list[i][j].right = bricks_list[i][j].left + BRICK_W - (20)
                        bricks_list[i][j].top = (WINDOW_HEIGHT) - 20 - (BRICK_H * j)
                        bricks_list[i][j].bottom = bricks_list[i][j].top - (BRICK_H) + 10
                        if bricks[i][j] == 1:
                            glColor3f(0.0, 1.0, 0.0)
                        elif bricks[i][j] == 2:
                            glColor3f(1.0, 1.0, 0.0)
                        elif bricks[i][j] == 3:
                            glColor3f(0.9, 0.5, 0.0)
                        elif bricks[i][j] == 4:
                            glColor3f(1.0, 0.0, 0.0)
                        draw_rect(bricks_list[i][j])
                        
            glColor3f(1.0, 1.0, 1.0)
            draw_circle(ball)
            draw_speed(abs(LAST_SPEED))

            if PAUSE:
                drawText("PAUSE", WINDOW_WIDTH/2 - 40, WINDOW_HEIGHT/2) 
                             
            draw_rect(player_1)

            if DEBUG:
                drawText("PADDLE: R: {0}, L: {1}, B: {2}, T: {3}, SPEED: {4}".format(player_1.right, player_1.left, player_1.bottom, player_1.top, LAST_SPEED), 200, 40, True)
                drawText("BALL: R: {0}, L: {1}, B: {2}, T: {3}".format(ball.right, ball.left, ball.bottom, ball.top), 200, 80, True)
                bricks_s = QTD_BRICKS_LVL * CURR_LEVEL
                drawText("BRICKS: TOTAL: {0} REMAINING: {1}".format(bricks_s, bricks_s - (SCORE - LAST_SCORE)), 200, 10, True)

        else:
            drawText("GAME OVER", WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2)
    else:
        drawText("YOU WON!!", WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2)
    glutSwapBuffers()
    

def main ():
    seed()
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("game")
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glutMouseFunc(onMouseButton)
    glutTimerFunc(redisplay_interval, timer, 1)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutPassiveMotionFunc(mouse)
    glutDisplayFunc(render)
    glutIdleFunc(render)
    glutMainLoop()


if __name__== "__main__":
  main()