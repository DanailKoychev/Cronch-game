# try:
import math

# except ImportError as message:
    # raise SystemExit(message)


class Vec2D:

    """2d vector class
    Supports the most common unary and binary scalar and vector operators,
    appart from cross product.

    """

    def __init__(self, x_or_pair=0, y=None):
        if y is None:
            self.x = x_or_pair[0]
            self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Invalid subscript {0} to Vec2D".format(key))

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Invalid subscript {0} to Vec2D".format(key))

    def __repr__(self):
        return 'Vec2D(%s, %s)' % (self.x, self.y)

    def __add__(self, other):
        if isinstance(other, Vec2D):
            return Vec2D(self.x + other.x, self.y + other.y)
        elif hasattr(other, "__getitem__"):
            return Vec2D(self.x + other[0], self.y + other[1])
        else:
            return Vec2D(self.x + other, self.y + other)

    __radd__ = __add__

    def __iadd__(self, other):
        if isinstance(other, Vec2D):
            self.x += other.x
            self.y += other.y
        elif hasattr(other, "__getitem__"):
            self.x += other[0]
            self.y += other[1]
        else:
            self.x += other
            self.y += other
        return self

    def __sub__(self, other):
        if isinstance(other, Vec2D):
            return Vec2D(self.x - other.x, self.y - other.y)
        elif (hasattr(other, "__getitem__")):
            return Vec2D(self.x - other[0], self.y - other[1])
        else:
            return Vec2D(self.x - other, self.y - other)

    def __rsub__(self, other):
        if isinstance(other, Vec2D):
            return Vec2D(other.x - self.x, other.y - self.y)
        elif (hasattr(other, "__getitem__")):
            return Vec2D(other[0] - self.x, other[1] - self.y)
        else:
            return Vec2D(other - self.x, other - self.y)

    def __isub__(self, other):
        if isinstance(other, Vec2D):
            self.x -= other.x
            self.y -= other.y
        elif (hasattr(other, "__getitem__")):
            self.x -= other[0]
            self.y -= other[1]
        else:
            self.x -= other
            self.y -= other
        return self

    def __mul__(self, other):
        if isinstance(other, Vec2D):
            return Vec2D(self.x * other.x, self.y * other.y)
        if (hasattr(other, "__getitem__")):
            return Vec2D(self.x * other[0], self.y * other[1])
        else:
            return Vec2D(self.x * other, self.y * other)

    __rmul__ = __mul__

    def __imul__(self, other):
        if isinstance(other, Vec2D):
            self.x *= other.x
            self.y *= other.y
        elif (hasattr(other, "__getitem__")):
            self.x *= other[0]
            self.y *= other[1]
        else:
            self.x *= other
            self.y *= other
        return self

    def __div__(self, other):
        if isinstance(other, Vec2D):
            return Vec2D(self.x / other.x, self.y / other.y)
        if (hasattr(other, "__getitem__")):
            return Vec2D(self.x / other[0], self.y / other[1])
        else:
            return Vec2D(self.x / other, self.y / other)

    __rdiv__ = __div__

    __truediv__ = __div__

    def __idiv__(self, other):
        if isinstance(other, Vec2D):
            self.x /= other.x
            self.y /= other.y
        elif (hasattr(other, "__getitem__")):
            self.x /= other[0]
            self.y /= other[1]
        else:
            self.x /= other
            self.y /= other
        return self

    def __neg__(self):
        return Vec2D(-self.x, -self.y)

    def __eq__(self, other):
        if hasattr(other, '__getitem__') and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        else:
            return False

    def __ne__(self, other):
        return not (self == other)

    def __nonzero__(self):
        return self.x or self.y

    def get_length(self):
        """Get the length of the vector.

        Vec2D.get_length(): return double

        """
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def set_length(self, value):
        """Set the length of the vector. Its direction will not be changed.

        Vec2D.set_length(value): return None

        """
        length = self.get_length()
        self.x *= value / length
        self.y *= value / length

    def get_angle(self):
        """Get the angle between the current vector and Vec2D(1, 0).

        Vec2D.get_angle(): return double

        """
        if self.get_length() == 0:
            return 0
        return math.degrees(math.atan2(self.y, self.x))

    def rotate(self, angle_degrees):
        """Rotate the vector maintaining its length.
        Positive angle_degrees rotate counterclockwise, negative -
        clockwise.

        Vec2D.rotate(angle_degrees): return None

        """
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        self.x = x
        self.y = y
