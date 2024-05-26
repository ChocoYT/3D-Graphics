import configparser
import keyboard
import pygame.mouse
import numpy as np
from os import getcwd

path = f"{getcwd()}"

# Config setup
defaults = configparser.ConfigParser()
defaults.read(f"{path}/defaults.ini")

screenWidth = int(defaults['screen']['width'])
screenHeight = int(defaults['screen']['height'])

class Camera():
    def __init__(self) -> None:
        self.x, self.y, self.z = 0, 0, 0
        self.xDir, self.yDir, self.zDir = 0, 0, 0

        self.moveX, self.moveY, self.moveZ = 0, 0, 0
        self.rotX, self.rotY, self.rotZ = 0, 0, 0

        self.moveSpeed = 0.1
        self.rotateSpeed = 1
        self.sensitivity = 0.15

    def update(self) -> None:
        # Creates movement variables
        moveX = int(keyboard.is_pressed("D")) - int(keyboard.is_pressed("A"))
        moveY = int(keyboard.is_pressed("Q")) - int(keyboard.is_pressed("E"))
        moveZ = int(keyboard.is_pressed("W")) - int(keyboard.is_pressed("S"))
        moveDist = np.sqrt((moveX ** 2) + (moveY ** 2) + (moveZ ** 2))

        if moveDist > 1:
            moveX /= moveDist
            moveY /= moveDist
            moveZ /= moveDist

        # Creates rotation variables
        rotX = int(keyboard.is_pressed("UP")) - int(keyboard.is_pressed("DOWN"))
        rotY = int(keyboard.is_pressed("RIGHT")) - int(keyboard.is_pressed("LEFT"))
        rotZ = int(keyboard.is_pressed("Z")) - int(keyboard.is_pressed("X"))

        rotDist = np.sqrt((rotX ** 2) + (rotY ** 2) + (rotZ ** 2))

        if rotDist > 1:
            rotX /= rotDist
            rotY /= rotDist
            rotZ /= rotDist

        # Accounts for mouse movement
        mouseMoveX, mouseMoveY = pygame.mouse.get_rel()
        if pygame.mouse.get_pressed()[2]:
            rotX -= mouseMoveY * self.sensitivity
            rotY += mouseMoveX * self.sensitivity

        # Calculates rotation
        self.rotX = -rotX * self.rotateSpeed
        self.rotY = rotY * self.rotateSpeed
        self.rotZ = -rotZ * self.rotateSpeed

        # Rotates camera
        self.xDir += self.rotX
        self.yDir += self.rotY
        self.zDir += self.rotZ

        self.xDir %= 360
        self.yDir %= 360
        self.zDir %= 360

        self.calculateTrigValues()

        # Calculates movement
        if moveX != 0:
            self.moveX = moveX * self.yDirCos
            self.moveY = moveX * self.xDirSin * self.yDirSin
            self.moveZ = moveX * self.yDirSin * self.zDirCos

        if moveY != 0:
            self.moveX += moveY * self.xDirCos * self.zDirSin
            self.moveY += moveY * self.yDirSin
            self.moveZ += moveY * self.xDirSin * self.zDirSin

        if moveZ != 0:
            self.moveX += moveZ * self.yDirSin * (self.zDirSin + 1)
            self.moveY += moveZ * self.xDirSin * self.yDirCos
            self.moveZ += moveZ * self.yDirCos
        
        # Multiplies by speed and inverts
        self.moveX *= self.moveSpeed
        self.moveY *= self.moveSpeed
        self.moveZ *= self.moveSpeed

        # Moves camera
        self.x += self.moveX
        self.y += self.moveY
        self.z += self.moveZ

    def calculateTrigValues(self) -> None:
        self.xDirSin = np.sin(np.deg2rad(self.xDir))
        self.xDirCos = np.cos(np.deg2rad(self.xDir))

        self.yDirSin = np.sin(np.deg2rad(self.yDir))
        self.yDirCos = np.cos(np.deg2rad(self.yDir))

        self.zDirSin = np.sin(np.deg2rad(self.zDir))
        self.zDirCos = np.cos(np.deg2rad(self.zDir))
        

camera = Camera()