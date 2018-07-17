class Point(object):
    def __init__(self, x, y=None):
        if isinstance(x, Point):
            self.x, self.y = x.x, x.y
        else:
            self.x = x
            self.y = y or x

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    def __mul__(self, other):
        return Point(self.x*other.x, self.y*other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
