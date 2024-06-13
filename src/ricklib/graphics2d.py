# 2D graphics library for ricklib

# Author: Rick Howell
# rick.howell.arts@gmail.com


import math
import random
import pngenerator as png
from enum import Enum


DEFAULT_MAX = 255
DEFAULT_BIT_DEPTH = 8
DEFAULT_WIDTH = 256
DEFAULT_HEIGHT = 256


class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (192, 192, 192)
    DARK_GRAY = (64, 64, 64)
    ORANGE = (255, 165, 0)
    PINK = (255, 192, 203)
    PURPLE = (128, 0, 128)
    BROWN = (165, 42, 42)


def angle2rgb(angle: float, bit_depth: int = DEFAULT_MAX) -> tuple:
    """Angle should be in radians from -pi to pi. \n
    Note: for vectors in R2, math.atan2(y, x) will give the angle."""

    if angle < -math.pi:
        angle = -math.pi
    elif angle > math.pi:
        angle = math.pi

    x = (angle + math.pi) / (2 * math.pi)

    r = int(bit_depth * ((1.0 + math.cos(2 * math.pi * x)) / 2.0))
    g = int(bit_depth * ((1.0 + math.cos(2 * math.pi * (x - 1/3))) / 2.0))
    b = int(bit_depth * ((1.0 + math.cos(2 * math.pi * (x - 2/3))) / 2.0))

    return (r, g, b)


def to_tuple(value: any, bit_depth: int = DEFAULT_MAX, binary: bool = True) -> tuple:
    if type(value) == float:
        return angle2rgb(value, bit_depth)
    
    if type(value) == int and binary:
        return (value * bit_depth, value * bit_depth, value * bit_depth)
    
    if type(value) == int and not binary:
        return (value, value, value)
    
    if type(value) == bool:
        if value:
            return (bit_depth, bit_depth, bit_depth)
        else:
            return (0, 0, 0)
        
    if type(value) == tuple:
        return value
    
    if type(value) == Color:
        return value.value


class Vector2:
    """A 2D vector class."""

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float):
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float):
        return Vector2(self.x / scalar, self.y / scalar)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return f'Vector2({self.x}, {self.y})'

    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        mag = self.magnitude()
        if mag != 0:
            self.x /= mag
            self.y /= mag

    def dot(self, other) -> float:
        return self.x * other.x + self.y * other.y

    def angle(self, other) -> float:
        return math.acos(self.dot(other) / (self.magnitude() * other.magnitude()))

    def rotate(self, angle: float):
        x = self.x * math.cos(angle) - self.y * math.sin(angle)
        y = self.x * math.sin(angle) + self.y * math.cos(angle)
        self.x = x
        self.y = y

    def lerp(self, other, t: float):
        return self + (other - self) * t

    def randomize(self, min: float = 0.0, max: float = 1.0):
        self.x = random.uniform(min, max)
        self.y = random.uniform(min, max)

    def copy(self):
        return Vector2(self.x, self.y)

    def to_tuple(self) -> tuple:
        return self.x, self.y
    
    def to_list(self) -> list:
        return [self.x, self.y]


class Line:
    '''A 2D line class.'''

    def __init__(self, start: Vector2, end: Vector2):
        self.start = start
        self.end = end

    def __str__(self):
        return f'{self.start} -> {self.end}'

    def __repr__(self):
        return f'Line({self.start}, {self.end})'

    def length(self) -> float:
        return (self.end - self.start).magnitude()

    def direction(self) -> Vector2:
        return (self.end - self.start).copy()

    def point_at(self, t: float) -> Vector2:
        '''Returns the point at t along the line. 0 <= t <= 1.'''
        return self.start + (self.end - self.start) * t

    def lerp(self, other, t: float):
        '''Returns a line that is t percent between self and other. 0 <= t <= 1.'''
        return Line(self.start.lerp(other.start, t), self.end.lerp(other.end, t))

    def copy(self):
        return Line(self.start.copy(), self.end.copy())
    


class Circle:
    '''A 2D circle class.'''

    def __init__(self, center: Vector2, radius: float):
        self.center = center
        self.radius = radius

    def __str__(self):
        return f'Center: {self.center}, Radius: {self.radius}'

    def __repr__(self):
        return f'Circle({self.center}, {self.radius})'

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def circumference(self) -> float:
        return 2 * math.pi * self.radius

    def contains(self, point: Vector2) -> bool:
        return (point - self.center).magnitude() <= self.radius

    def copy(self):
        return Circle(self.center.copy(), self.radius)



class Frame:
    '''A 2D frame in the form of a rectangular list of lists.'''

    def __init__(self, width: int = DEFAULT_WIDTH, height: int = DEFAULT_HEIGHT, bit_depth: int = DEFAULT_BIT_DEPTH):
        self.width = width
        self.height = height
        self.bit_depth = bit_depth
        self.frame = [[to_tuple(Color.BLACK) for _ in range(width)] for _ in range(height)]

    def __str__(self):
        return f'Frame({self.width}, {self.height})'
    
    def __repr__(self):
        return f'Frame({self.width}, {self.height})'
    
    def __getitem__(self, key: tuple):
        return self.frame[key[1]][key[0]]
    
    def __setitem__(self, key: tuple, value: any):
        self.frame[key[1]][key[0]] = to_tuple(value, self.bit_depth, binary=False)

    def fill(self, color: any):
        for y in range(self.height):
            for x in range(self.width):
                self.frame[y][x] = to_tuple(color, self.bit_depth, binary=False)
    
    def get_frame(self) -> list:
        return self.frame
    
    def print_frame(self):
        for row in self.frame:
            print(row)

    def export(self, filename: str):
        picture = png.RGB(filename, self.frame, self.bit_depth)
        picture.make()
    
    def draw_line(self, start: tuple, end: tuple, color: any = Color.BLACK, width: int = 1):
        '''Draws a line from start to end with color and specified width.
        Start and end are tuples of the form (x, y).'''

        color = to_tuple(color, self.bit_depth, binary=False)
        x1, y1 = start
        x2, y2 = end

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        x = x1
        y = y1
        sx = 1 if x2 > x1 else -1
        sy = 1 if y2 > y1 else -1
        if dx > dy:
            err = dx / 2.0
            while x != x2:
                for i in range(-width // 2, width // 2 + 1):
                    if 0 <= y + i < self.height:
                        try:
                            self[x, y + i] = color
                        except:
                            pass
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != y2:
                for i in range(-width // 2, width // 2 + 1):
                    if 0 <= x + i < self.width:
                        try:
                            self[x + i, y] = color
                        except:
                            pass
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy
        for i in range(-width // 2, width // 2 + 1):
            if 0 <= x + i < self.width:
                try:
                    self[x + i, y] = color
                except:
                    pass

    def draw_circle(self, center: tuple, radius: float, color: any = Color.BLACK):
        '''Draws a circle with center, radius, color, and width.'''
        
        color = to_tuple(color, self.bit_depth, binary=False)
        x0, y0 = center
        x = radius
        
        for y in range(y0 - radius, y0 + radius + 1):
            for x in range(x0 - radius, x0 + radius + 1):
                if (x - x0) ** 2 + (y - y0) ** 2 <= radius ** 2:
                    try:
                        self[x, y] = color
                    except:
                        pass



def test():
    v1 = Vector2(1, 2)
    v2 = Vector2(3, 4)
    print(v1 + v2)
    print(v1 - v2)
    print(v1 * 2)
    print(v1 / 2)
    print(v1.magnitude())
    v1.normalize()
    print(v1)
    print(v1.dot(v2))
    print(v1.angle(v2))
    v1.rotate(math.pi / 2)
    print(v1)
    print(v1.lerp(v2, 0.5))
    v1.randomize()
    print(v1)
    print(v1.to_tuple())
    print(v1.to_list())

    l = Line(Vector2(0, 0), Vector2(1, 1))
    print(l)
    print(l.length())
    print(l.direction())
    print(l.point_at(0.5))
    print(l.lerp(Line(Vector2(2, 2), Vector2(3, 3)), 0.5))
    l2 = l.copy()
    print(l2)

    c = Circle(Vector2(0, 0), 1)
    print(c)
    print(c.area())

    f = Frame(8, 8)
    print(f)
    print(f.get_frame())
    f.fill(Color.WHITE)
    print(f.get_frame())
    f[1, 1] = Color.BLACK
    f.print_frame()
    print(f[1, 1])
    f[1, 1] = Color.WHITE

    f.draw_line((0, 0), (7, 7), Color.BLACK)
    f.draw_line((0, 4), (3, 0), Color.CYAN)
    f.export('tests/frame_1test.png')

    g = Frame(256, 256)
    g.fill(Color.WHITE)
    g.draw_line((0, 0), (255, 255), Color.BLACK, width = 4)
    g.draw_circle((128, 128), 128, Color.RED)
    g.draw_circle((128, 128), 96, Color.GREEN)
    g.draw_circle((128, 128), 64, Color.BLUE)
    g.export('tests/frame_2test.png')




if __name__ == '__main__':
    test()