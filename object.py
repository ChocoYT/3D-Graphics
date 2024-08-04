from configparser import ConfigParser
import numpy
from OpenGL.GL import *
from OpenGL.GLU import *
from os import getcwd

path = getcwd()

defaults = ConfigParser()
defaults.read(f"{path}\\defaults.ini")

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
        [(0, 1, 2), (1.0, 0.0, 0.0)],
        [(0, 2, 3), (1.0, 0.0, 0.0)],
        [(4, 5, 6), (1.0, 0.5, 0.0)],
        [(4, 6, 7), (1.0, 0.5, 0.0)],
        [(0, 1, 4), (1.0, 1.0, 0.0)],
        [(1, 4, 5), (1.0, 1.0, 0.0)],
        [(1, 2, 5), (0.0, 1.0, 0.0)],
        [(2, 5, 6), (0.0, 1.0, 0.0)],
        [(2, 3, 6), (0.0, 0.0, 1.0)],
        [(3, 6, 7), (0.0, 0.0, 1.0)],
        [(3, 4, 7), (1.0, 1.0, 1.0)],
        [(0, 3, 4), (1.0, 1.0, 1.0)],
    ]

    def __init__(self, scale: int | float = 1) -> None:
        self.edges = Object.edges
        self.vertices = list(numpy.multiply(numpy.array(Object.vertices), scale))
        self.surfaces = Object.surfaces

        self.wireframe = False

    def translate(self, x: int, y: int, z: int) -> None:
        self.vertices = list(map(lambda vertex: (vertex[0] + x, vertex[1] + y, vertex[2] + -z), self.vertices))

    def draw(self) -> None:
        self.outline()
        if not self.wireframe:
            self.fill()

    def fill(self) -> None:
        glBegin(GL_TRIANGLES)
        for vertices, colour in self.surfaces:
            glColor3f(*colour)
            for vertex in vertices:
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