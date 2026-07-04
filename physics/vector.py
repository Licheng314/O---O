"""
physics/vector.py
2D 向量工具
"""

import math


class Vector2:
    """轻量 2D 向量"""

    __slots__ = ('x', 'y')

    def __init__(self, x=0.0, y=0.0):
        if isinstance(x, (list, tuple)):
            self.x = float(x[0])
            self.y = float(x[1])
        else:
            self.x = float(x)
            self.y = float(y)

    def copy(self):
        return Vector2(self.x, self.y)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector2(self.x / scalar, self.y / scalar)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def length_squared(self):
        return self.x * self.x + self.y * self.y

    def normalized(self):
        length = self.length()
        if length > 0:
            return Vector2(self.x / length, self.y / length)
        return Vector2(0, 0)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def rotate(self, angle_rad):
        """旋转向量"""
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        return Vector2(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a
        )

    def to_tuple(self):
        return (self.x, self.y)

    def __repr__(self):
        return f"Vector2({self.x:.1f}, {self.y:.1f})"


def rotate_vector(v, angle_rad):
    """旋转向量（无对象版本）"""
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    return Vector2(
        v.x * cos_a - v.y * sin_a,
        v.x * sin_a + v.y * cos_a
    )
