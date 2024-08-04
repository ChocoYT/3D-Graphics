from configparser import ConfigParser
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from os import getcwd

from camera import camera as cam
from object import Object

from pygame.locals import OPENGL, DOUBLEBUF
pygame.init()

path = getcwd()

# Config setup
defaults = ConfigParser()
defaults.read(f"{path}\\defaults.ini")

# Config variables
screenWidth = int(defaults['screen']['width'])
screenHeight = int(defaults['screen']['height'])
FPS = int(defaults['screen']['FPS'])

FOV = float(defaults['screen']['FOV'])

zNear = float(defaults['screen']['zNear'])
zFar = float(defaults['screen']['zFar'])

# Screen setup
pygame.display.set_mode((screenWidth, screenHeight), DOUBLEBUF | OPENGL)
pygame.display.set_caption(defaults['screen']['name'])
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

# Add perspective and depth
aspectRatio = screenWidth / screenHeight
gluPerspective(FOV * aspectRatio / 2, aspectRatio, zNear, zFar)
glEnable(GL_DEPTH_TEST)

obj = Object(scale=2)

run = True
while run:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run = False
        if event.type == pygame.QUIT:
            run = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Update camera
    cam.update()
    # Pointer lock
    pygame.mouse.set_pos((screenWidth / 2, screenHeight / 2))

    # Translate vertices in buffer
    obj.translate(-cam.moveX, -cam.moveY, -cam.moveZ)

    # Rotate vertices in buffer
    glRotatef(cam.objRotX, 1, 0, 0)
    glRotatef(cam.objRotY, 0, 1, 0)
    glRotatef(cam.objRotZ, 0, 0, 1)
    print(f"{cam.xDir}, {cam.yDir}, {cam.zDir}")
    obj.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
quit()