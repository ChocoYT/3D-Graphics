from configparser import ConfigParser
import keyboard
from pygame import mouse, Vector3
import numpy as np
from os import getcwd

path = getcwd()

# Config setup
defaults = ConfigParser()
defaults.read(f"{path}\\defaults.ini")

screenWidth = int(defaults['screen']['width'])
screenHeight = int(defaults['screen']['height'])

class Camera():
    def __init__(self) -> None:
        self.x, self.y, self.z = 0, 0, 0
        self.xDir, self.yDir, self.zDir = 0, 0, 0

        self.moveX, self.moveY, self.moveZ = 0, 0, 0
        self.rotX, self.rotY, self.rotZ = 0, 0, 0

        self.objRotX, self.objRotY, self.objRotZ = 0, 0, 0

        self.moveSpeed = 0.1
        self.rotateSpeed = 1
        self.sensitivity = 0.15

    def update(self) -> None:
        self.calculateTrigValues()

        # Creates rotation variables
        rotX = int(keyboard.is_pressed("UP")) - int(keyboard.is_pressed("DOWN"))
        rotY = int(keyboard.is_pressed("RIGHT")) - int(keyboard.is_pressed("LEFT"))
        rotZ = int(keyboard.is_pressed("Z")) - int(keyboard.is_pressed("X"))

        # Accounts for mouse movement
        mouseMoveX, mouseMoveY = mouse.get_rel()
        if mouse.get_pressed()[2]:
            rotX += mouseMoveY * self.sensitivity
            rotY += mouseMoveX * self.sensitivity

        rotateVector = Vector3(rotX, rotY, rotZ)
        if rotateVector.length() > 1:
            rotateVector.normalize()

        self.rotate(rotateVector)

        # Creates movement variables
        moveX = int(keyboard.is_pressed("D")) - int(keyboard.is_pressed("A"))
        moveY = int(keyboard.is_pressed("Q")) - int(keyboard.is_pressed("E"))
        moveZ = int(keyboard.is_pressed("W")) - int(keyboard.is_pressed("S"))

        moveVector = Vector3(moveX, moveY, moveZ)
        if moveVector.length() > 1:
            moveVector.normalize()

        self.move(moveVector)


    def move(self, vector: Vector3) -> None:
        self.moveX, self.moveY, self.moveZ = 0, 0, 0

        # Calculates movement
        if vector.x != 0:
            self.moveX += vector.x * self.yDirCos * self.zDirCos
            self.moveY -= vector.x * self.xDirCos * self.zDirSin
            self.moveZ -= vector.x * self.xDirCos * self.yDirSin

        if vector.y != 0:
            self.moveX += vector.y * self.yDirCos * self.zDirSin
            self.moveY += vector.y * self.xDirCos * self.zDirCos
            self.moveZ += vector.y * self.xDirSin * self.yDirCos

        if vector.z != 0:
            self.moveX += vector.z * self.yDirSin * self.zDirCos
            self.moveY -= vector.z * self.xDirSin * self.zDirCos
            self.moveZ += vector.z * self.xDirCos * self.yDirCos

        # Multiplies by speed
        self.moveX *= self.moveSpeed
        self.moveY *= self.moveSpeed
        self.moveZ *= self.moveSpeed

        # Moves camera
        self.x += self.moveX
        self.y += self.moveY
        self.z += self.moveZ

    def rotate(self, vector: Vector3) -> None:
        self.rotX = vector.x
        self.rotY = vector.y
        self.rotZ = vector.z

        '''
        # Calculates object rotation
        self.objRotX, self.objRotY, self.objRotZ = 0, 0, 0

        # Rotation looking at X
        self.objRotX += self.rotZ * self.xDirCos * self.yDirSin * self.zDirCos   # Rotation looking at +- X (xDir = 0 / 180)
        self.objRotY += self.rotY * self.xDirCos * self.yDirSin * self.zDirCos

        self.objRotX += self.rotY * self.xDirSin * self.yDirSin * self.zDirCos   # Rotation looking at +- X (xDir = 90 / 270)
        self.objRotY += self.rotZ * self.xDirSin * self.yDirSin * self.zDirCos

        self.objRotZ += self.rotX * self.yDirSin * self.zDirCos                  # Rotation at +- X

        # Rotation looking at Y
        self.objRotX += self.rotX * self.xDirCos * self.yDirCos * self.zDirCos   # Rotation looking at +- Y (yDir = 0 / 180)
        self.objRotY += self.rotZ * self.xDirCos * self.yDirCos * self.zDirCos

        self.objRotX += self.rotZ * self.xDirCos * self.yDirSin * self.zDirCos   # Rotation looking at +- Y (yDir = 90 / 270)
        self.objRotY += self.rotX * self.xDirCos * self.yDirSin * self.zDirCos

        self.objRotZ += self.rotY * self.xDirCos * self.zDirCos                  # Rotation at +- Y

        # Rotation looking at Z
        self.objRotX += self.rotX * self.xDirCos * self.yDirCos * self.zDirCos   # Rotation looking at +- Z (zDir = 0 / 180)
        self.objRotY += self.rotY * self.xDirCos * self.yDirCos * self.zDirCos

        self.objRotX += self.rotY * self.xDirCos * self.yDirCos * self.zDirSin   # Rotation looking at +- Z (zDir = 90 / 270)
        self.objRotY += self.rotX * self.xDirCos * self.yDirCos * self.zDirSin

        self.objRotZ += self.rotZ * self.xDirCos * self.yDirCos                  # Rotation at +- Z
        '''
        self.objRotX, self.objRotY, self.objRotZ = self.rotX, self.rotY, self.rotZ


        # Calculates rotation
        self.rotX *= self.rotateSpeed
        self.rotY *= self.rotateSpeed
        self.rotZ *= self.rotateSpeed

        # Rotates camera
        self.xDir += self.rotX
        self.yDir += self.rotY
        self.zDir += self.rotZ

        self.xDir %= 360
        self.yDir %= 360
        self.zDir %= 360


    def calculateTrigValues(self) -> None:
        self.xDirSin = np.sin(np.deg2rad(self.xDir))
        self.xDirCos = np.cos(np.deg2rad(self.xDir))

        self.yDirSin = np.sin(np.deg2rad(self.yDir))
        self.yDirCos = np.cos(np.deg2rad(self.yDir))

        self.zDirSin = np.sin(np.deg2rad(self.zDir))
        self.zDirCos = np.cos(np.deg2rad(self.zDir))
        

camera = Camera()