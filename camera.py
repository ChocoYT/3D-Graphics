import configparser
import pygame.mouse
import numpy as np
from os import getcwd
from pynput import keyboard

path = getcwd()

# Config setup
defaults = configparser.ConfigParser()
defaults.read(f"{path}/defaults.ini")

screenWidth = int(defaults['screen']['width'])
screenHeight = int(defaults['screen']['height'])

# Dictionary to keep track of key states
key_state = {}

def on_press(key):
    try:
        key_state[key.char] = True
    except AttributeError:
        key_state[key] = True

def on_release(key):
    try:
        key_state[key.char] = False
    except AttributeError:
        key_state[key] = False

# Start the listener in a non-blocking way
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

def is_pressed(key):
    # Handle special keys
    if isinstance(key, keyboard.Key):
        return key_state.get(key, False)
    # Handle character keys
    else:
        return key_state.get(key, False)

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
        
        moveX = int(is_pressed("D")) - int(is_pressed("A")) # Ew
        moveY = int(is_pressed("Q")) - int(is_pressed("E")) # Ew
        moveZ = int(is_pressed("W")) - int(is_pressed("S")) # Ew
        moveDist = np.sqrt((moveX ** 2) + (moveY ** 2) + (moveZ ** 2))

        if moveDist > 1:
            moveX /= moveDist
            moveY /= moveDist
            moveZ /= moveDist

        # Creates rotation variables
        rotX = int(is_pressed(keyboard.Key.up)) - int(is_pressed(keyboard.Key.down)) # Ew
        rotY = int(is_pressed(keyboard.Key.right)) - int(is_pressed(keyboard.Key.left)) # Ew
        rotZ = int(is_pressed("Z")) - int(is_pressed("X")) # Ew

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
            self.moveX += moveZ * self.yDirSin * self.zDirSin
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