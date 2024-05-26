import configparser
import numpy
from OpenGL.GL import *
from OpenGL.GLU import *

path = f".\\3D Graphics\\"

defaults = configparser.ConfigParser()
defaults.read(f"{path}defaults.ini")

fillColour = tuple(map(float, defaults['object']['fillColour'].split(", ")))

outlineColour = tuple(map(float, defaults['object']['outlineColour'].split(", ")))
outlineWidth = int(defaults['object']['outlineWidth'])


class Object():
    vertices = [
       (-1,  1, -1),
       (-1,  1,  1),
       (1,   1,  1),
       (1,   1, -1),
       (-1, -1, -1),
       (-1, -1,  1),
       (1,  -1,  1),
       (1,  -1, -1),
    ]
    edges = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),
    ]
    surfaces = [
        (0, 1, 2),
        (0, 2, 3),
        (4, 5, 6),
        (4, 6, 7),
        (0, 1, 4),
        (1, 4, 5),
        (1, 2, 5),
        (2, 5, 6),
        (2, 3, 6),
        (3, 6, 7),
        (3, 4, 7),
        (4, 7, 0),
    ]

    def __init__(self, scale: int | float = 1) -> None:
        self.edges = Object.edges
        self.vertices = list(numpy.multiply(numpy.array(Object.vertices), scale))
        self.surfaces = Object.surfaces

    def translate(self, x: int, y: int, z: int) -> None:
        self.vertices = list(map(lambda vertex: (vertex[0] + x, vertex[1] + y, vertex[2] + z), self.vertices))

    def draw(self) -> None:
        self.outline()
        self.fill()

    def fill(self) -> None:
        glBegin(GL_TRIANGLES)
        for surface in self.surfaces:
            for vertex in surface:
                glColor3f(*fillColour)
                glVertex3fv(self.vertices[vertex])
        glEnd()

    def outline(self) -> None:
        glLineWidth(outlineWidth)

        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glColor3f(*outlineColour)
                glVertex3fv(self.vertices[vertex])
        glEnd()