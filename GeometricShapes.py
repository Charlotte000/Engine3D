from Engine3D import Engine
from data.vector import Vector
from math import pi, sin, cos
from requests import get
import numpy


class Cube(Engine.Object):
    def __init__(self, center, size):
        """
        Creates cube

        :param list center:
        :param float size:
        """
        self.points, self.lines, self.surfaces = Cube.create(size)
        self.size = size
        super().__init__(center)

    @staticmethod
    def create(width):
        points = [
            Vector(-.5, -.5, -.5),
            Vector(.5, -.5, -.5),
            Vector(.5, .5, -.5),
            Vector(-.5, .5, -.5),
            Vector(-.5, -.5, .5),
            Vector(.5, -.5, .5),
            Vector(.5, .5, .5),
            Vector(-.5, .5, .5),
        ]

        for i in range(len(points)):
            points[i] *= width

        lines = []
        for i in range(4):
            lines.append([i, (i + 1) % 4])
            lines.append([i + 4, (i + 1) % 4 + 4])
            lines.append([i, i + 4])

        surfaces = [[0, 1, 2, 3], [4, 5, 6, 7], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7], [0, 1, 5, 4]]

        return points, lines, surfaces


class Sphere(Engine.Object):
    def __init__(self, center, radius, detail):
        """
        Creates sphere

        :param list center:
        :param float radius:
        :param int detail:
        """
        self.radius = radius
        self.points, self.lines, self.surfaces = Sphere.create(detail, radius)
        super().__init__(center)

    @staticmethod
    def create(detail, radius):
        points = []
        lines = []
        surfaces = []

        detail -= 1
        figure_map = [[None for i in range(detail + 1)] for j in range(detail + 1)]
        for i in range(detail + 1):
            for j in range(detail + 1):
                angle1 = i / detail * pi
                angle2 = j / detail * 2 * pi
                x = sin(angle1) * cos(angle2)
                y = sin(angle1) * sin(angle2)
                z = cos(angle1)
                v = Vector(x, y, z)
                v *= radius
                points.append(v)
                figure_map[i][j] = points.index(v)

        for i in range(detail):
            for j in range(detail):
                index1 = figure_map[i][j]
                index2 = figure_map[i][j + 1]
                index3 = figure_map[i + 1][j + 1]
                index4 = figure_map[i + 1][j]
                surfaces.append([index1, index2, index3, index4])
                lines.extend([[index1, index2], [index2, index3], [index3, index4]])

        return points, lines, surfaces


class Mesh(Engine.Object):
    def __init__(self, center, size, detail):
        """
        Creates mesh

        :param list center:
        :param float size:
        :param int detail:
        """
        self.size = size
        self.detail = detail
        self.points, self.lines, self.surfaces = Mesh.create(detail, size)
        super().__init__(center)

    @staticmethod
    def create(detail, size):
        width = size / detail
        points = [Vector((x - detail / 2) * width, (y - detail / 2) * width, 0)
                  for y in range(detail)
                  for x in range(detail)]
        lines = []
        surfaces = []
        for y in range(detail - 1):
            for x in range(detail - 1):
                lines.append([x + y * detail, x + 1 + y * detail])
                lines.append([x + y * detail, x + (y + 1) * detail])
                surfaces.append([x + y * detail, x + 1 + y * detail, x + 1 + (y + 1) * detail, x + (y + 1) * detail])
        for x in range(detail):
            for y in range(detail - 1):
                lines.append([x + y * detail, x + (y + 1) * detail])
        for x in range(detail - 1):
            for y in range(detail):
                lines.append([x + 1 + y * detail, x + y * detail])
        return points, lines, surfaces


class MobiusStrip(Engine.Object):
    def __init__(self, center, size, detail):
        """
        Creates Modious strip

        :param list center:
        :param float size:
        :param int detail:
        """
        self.size = size
        self.points, self.lines, self.surfaces = MobiusStrip.create(detail, size)
        super().__init__(center)

    @staticmethod
    def create(detail, scale):
        points = []
        lines = []
        surfaces = []

        for u0 in range(detail):
            for v0 in range(detail):
                u = u0 / detail * 2 * pi
                v = v0 / detail * 2 - 1

                x = (1 + v / 2 * cos(u / 2)) * cos(u)
                y = (1 + v / 2 * cos(u / 2)) * sin(u)
                z = v / 2 * sin(u / 2)

                points.append(Vector(x * scale, y * scale, z * scale))

        for u in range(detail):
            for v in range(detail - 1):
                lines.append([u + v * detail, u + (v + 1) * detail])
                if u + 1 < detail:
                    lines.append([u + v * detail, u + 1 + v * detail])
                    surfaces.append(
                        [u + v * detail, u + (v + 1) * detail, u + 1 + (v + 1) * detail, u + 1 + v * detail])

        for u in range(detail):
            lines.append([u + (detail - 1) * detail, abs(u - detail + 1)])
            if u + 1 < detail:
                surfaces.append([u + (detail - 1) * detail, u + 1 + (detail - 1) * detail,
                                 detail - u - 2, detail - u - 1])

        return points, lines, surfaces


class Torus(Engine.Object):
    def __init__(self, center, radius_min, radius_max, detail):
        """
        Creates torus

        :param list center:
        :param float radius_min:
        :param float radius_max:
        :param int detail:
        """
        self.radius_min, self.radius_max = radius_min, radius_max
        self.points, self.lines, self.surfaces = Torus.create(detail, radius_max, radius_min)
        super().__init__(center)

    @staticmethod
    def create(detail, radius_max, radius_min):
        points = []
        lines = []
        surfaces = []
        for i in range(detail):
            for j in range(detail):
                f = i / detail * 2 * pi
                u = j / detail * 2 * pi - pi

                x = (radius_max + radius_min * cos(u)) * cos(f)
                y = (radius_max + radius_min * cos(u)) * sin(f)
                z = radius_min * sin(u)
                points.append(Vector(x, y, z))

        for i in range(detail):
            for j in range(detail):
                indexi = i + 1
                indexj = j + 1
                if indexi >= detail:
                    indexi = 0
                if indexj >= detail:
                    indexj = 0
                lines.append([i + j * detail, indexi + j * detail])
                lines.append([i + j * detail, i + indexj * detail])
                surfaces.append([i + j * detail, indexi + j * detail, indexi + indexj * detail, i + indexj * detail])

        return points, lines, surfaces


class KleinBottle(Engine.Object):
    def __init__(self, center, size, detail):
        """
        Creates Klein bottle

        :param list center:
        :param float size:
        :param int detail:
        """
        self.size = size
        self.points, self.lines, self.surfaces = KleinBottle.create(detail, size)
        super().__init__(center)

    @staticmethod
    def create(detail, scale):
        points = []
        lines = []
        surfaces = []

        for i in range(detail):
            for j in range(detail):
                u = i / detail * pi
                v = j / detail * 2 * pi

                x = -2 / 15 * cos(u) * (3 * cos(v) - 30 * sin(u) + 90 * pow(cos(u), 4) * sin(u) - 60 * pow(cos(u), 6) *
                                        sin(u) + 5 * cos(u) * cos(v) * sin(u))
                y = -1 / 15 * sin(u) * (3 * cos(v) - 3 * pow(cos(u), 2) * cos(v) - 48 * pow(cos(u), 4) * cos(v) + 48 *
                                        pow(cos(u), 6) * cos(v) - 60 * sin(u) + 5 * cos(u) * cos(v) * sin(u) - 5 *
                                        pow(cos(u), 3) * cos(v) * sin(u) - 80 * pow(cos(u), 5) * cos(v) * sin(u) + 80 *
                                        pow(cos(u), 7) * cos(v) * sin(u))
                z = 2 / 15 * (3 + 5 * cos(u) * sin(u)) * sin(v)
                points.append(Vector(x * scale, y * scale, z * scale))

        for i in range(detail):
            for j in range(detail - 1):
                lines.append([i + j * detail, (i + 1) % detail + j * detail])
                lines.append([i + j * detail, i + (j + 1) * detail])

                surfaces.append([i + j * detail, (i + 1) % detail + j * detail, (i + 1) % detail + (j + 1) * detail,
                                 i + (j + 1) * detail])
        return points, lines, surfaces


class UtahTeapot(Engine.Object):
    def __init__(self, center, size):
        """
        Creates utah teapot

        :param list center:
        :param float size:
        """
        self.size = size
        self.points, self.surfaces = UtahTeapot.create(size)
        self.lines = [[i, i+1] for i in range(0, len(self.points) - 1)]
        super().__init__(center)

    @staticmethod
    def create(scale):
        points = []
        surfaces = []

        data = get('https://graphics.stanford.edu/courses/cs148-10-summer/as3/code/as3/teapot.obj').text.split('\n')
        for i in data:
            try:
                if i[:1] == 'v':
                    x, y, z = i[2:].split(' ')
                    points.append(Vector(float(x), -float(y), float(z)))
                if i[:1] == 'f':
                    surfaces.append(
                        [int(item.split('/')[0]) - 1 for item in i[2:].split(' ') if item.split('/')[0].isdigit()])
            except:
                pass
        for i in range(len(points)):
            points[i] *= scale
        return points, surfaces


class FileObject(Engine.Object):
    def __init__(self, center, filename, size=1):
        """
        Creates object from .obj file

        :param list center:
        :param str filename:
        :param float size:
        """
        self.size = size
        self.points, self.surfaces = FileObject.load(filename, size)
        self.lines = [[i, i+1] for i in range(0, len(self.points) - 1)]
        super().__init__(center)

    @staticmethod
    def load(filename, scale):
        figure = []
        surfaces = []

        with open(filename, 'r') as file:
            data = file.read().split('\n')
            for i in data:
                try:
                    if i[:1] == 'v':
                        x, y, z = i[2:].split(' ')
                        figure.append(Vector(float(x), -float(y), float(z)))
                    if i[:1] == 'f':
                        surfaces.append(
                            [int(item.split('/')[0]) - 1 for item in i[2:].split(' ') if item.split('/')[0].isdigit()])
                except:
                    pass

        for i in range(len(figure)):
            figure[i] *= scale
        return figure, surfaces


class UniformSphere(Engine.Object):
    def __init__(self, center, radius, detail):
        """
        Creates a uniform sphere

        :param list center:
        :param float radius:
        :param int detail:
        """
        self.points, self.lines, self.surfaces = UniformSphere.create(radius, detail)
        self.radius = radius
        super().__init__(center)

    @staticmethod
    def create(radius, detail):
        indices = numpy.arange(0, detail, dtype=float) + 0.5

        phi = numpy.arccos(1 - 2*indices/detail)
        theta = pi * (1 + 5**0.5) * indices

        x, y, z = numpy.cos(theta) * numpy.sin(phi), numpy.sin(theta) * numpy.sin(phi), numpy.cos(phi);
        points = []

        for i in range(len(x)):
            points.append(Vector(int(x[i] * radius), int(y[i] * radius), int(z[i] * radius)))

        lines = [[i , i + 3] for i in range(detail - 3)]
        return points, lines, None
