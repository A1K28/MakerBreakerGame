from typing import List

from app.game.components.star_expansion import Star
from app.game.config.types import Point2D
from app.game.config.utils import distance, offset, midpoint, draw_quadratic_bezier


class Edge:
    def __init__(self, points: List[Point2D]):
        self.points = points

    def draw(self, node_radius):
        if self.points is None or len(self.points) < 2:
            raise ValueError(f"Invalid point array passed ar argument: {self.points}")
        elif len(self.points) == 2:
            p0, p2 = self.points[0], self.points[1]
            self._draw2d(p0, p2)
        else:
            mid = self.points[0]
            for i in range(1, len(self.points)):
                mid = midpoint(mid, self.points[i])
            for point in self.points:
                self._draw2d(point, mid)
            star = Star(mid.x, mid.y, 6)
            star.draw(node_radius)

    def _draw2d(self, p0:Point2D, p2: Point2D):
        dist = distance(p0, p2)
        off = offset(dist)
        mid = midpoint(p0, p2)
        p1 = Point2D(mid.x + off, mid.y + off)
        draw_quadratic_bezier(p0, p1, p2)
