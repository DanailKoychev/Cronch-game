class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return str((self.x, self.y))

    def __add__(self, vector):
        return Point(self.x + vector.x, self.y + vector.y)

    def __iadd__(self, vector):
        self.x += vector.x
        self.y += vector.y
        return self

    def __eq__(self, point):
        return self.x == point.x and self.y == point.y