class Point(object):
    def __init__(self, x, y=None):
        if isinstance(x, Point):
            self.x, self.y = x.x, x.y
        else:
            self.x = x
            self.y = x if y is None else y

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    def __mul__(self, other):
        return Point(self.x*other.x, self.y*other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return 'p({} {})'.format(self.x, self.y)

    def __repr__(self):
        return str(self)

    def __bool__(self):
        return 0 <= self.x <= 7 and 0 <= self.y <= 7
