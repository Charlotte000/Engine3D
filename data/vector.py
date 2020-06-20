from math import sqrt, cos, sin, atan2, degrees, radians
from random import uniform


class Vector:
    DEGREES = False

    def __init__(self, x=0, y=0, z=0):
        if type(x) in [list, tuple]:
            if len(x) == 1:
                self.x = x[:]
                self.y = self.z = 0
            elif len(x) == 2:
                self.x, self.y = x[:]
                self.z = 0
            elif len(x) == 3:
                self.x, self.y, self.z = x[:]
        else:
            self.x = x
            self.y = y
            self.z = z

    def setLength(self, length):
        ve = self.copy()
        if ve.length() > 0:
            ve *= length / ve.length()
            self.x, self.y, self.z = ve.x, ve.y, ve.z
        return self

    def length(self):
        return sqrt(pow(self.x, 2) + pow(self.y, 2) + pow(self.z, 2))

    def angle(self):
        a = atan2(self.y, self.x)
        if Vector.DEGREES:
            return degrees(a)
        return a

    def setAngle(self, angle):
        v = Vector.fromAngle(angle)
        v *= self.length()
        self.x = v.x
        self.y = v.y
        return self

    def rotate(self, angle):
        if Vector.DEGREES:
            angle = radians(angle)
        x = self.x * cos(angle) - self.y * sin(angle)
        y = self.x * sin(angle) + self.y * cos(angle)

        self.x, self.y = x, y
        return self

    def copy(self):
        return Vector(self.x, self.y, self.z)

    def constrain(self, minValue, maxValue):
        le = self.length()
        if le > maxValue:
            self.setLength(maxValue)
        elif le < minValue:
            self.setLength(minValue)
        return self
    
    @staticmethod
    def fromPoints(point1, point2):
        return Vector(*point2) - Vector(*point1)

    @staticmethod
    def fromAngle(angle):
        v = Vector(1, 0)
        v.rotate(angle)
        return v
    
    @staticmethod
    def average(*vectors):
        v = Vector()
        for vec in vectors:
            v += vec
        v /= len(vectors)
        return v

    @staticmethod
    def random2D():
        a = Vector(uniform(-1, 1), uniform(-1, 1))
        a.setLength(1)
        return a

    @staticmethod
    def random3D():
        a = Vector(uniform(-1, 1), uniform(-1, 1), uniform(-1, 1))
        a.setLength(1)
        return a
    
    @staticmethod
    def angleBetween(v1, v2):
        a = atan2(v1.x * v2.y - v1.y * v2.x, v1.x * v2.x + v1.y * v2.y)
        if Vector.DEGREES:
            return degrees(a)
        return a

    def __add__(self, vector):
        v = self.copy()
        v.x += vector.x
        v.y += vector.y
        v.z += vector.z
        return v

    def __sub__(self, vector):
        v = self.copy()
        v.x -= vector.x
        v.y -= vector.y
        v.z -= vector.z
        return v

    def __mul__(self, number):
        v = self.copy()
        v.x *= number
        v.y *= number
        v.z *= number
        return v

    def __truediv__(self, number):
        v = self.copy()
        v.x /= number
        v.y /= number
        v.z /= number
        return v

    def __str__(self):
        return f'Vector[{self.x}, {self.y}, {self.z}]'

    def __getitem__(self, item):
        return [self.x, self.y, self.z][item]

    def __setitem__(self, item, value):
        if item == 0:
            self.x = value
        elif item == 1:
            self.y = value
        elif item == 2:
            self.z = value
        else:
            raise IndexError

    def __round__(self):
        return Vector(round(self.x), round(self.y), round(self.z))

    def __iter__(self):
        return iter([self.x, self.y, self.z])

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        return False

    def __lt__(self, vector):
        return self.length() < vector.length()

    def __le__(self, vector):
        return (self < vector) or (self == vector)
