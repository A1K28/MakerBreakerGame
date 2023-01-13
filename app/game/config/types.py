from typing import NamedTuple


class Point2D(NamedTuple):
    x: float
    y: float

    def __int__(self, x, y):
        self.x = x
        self.y = y
