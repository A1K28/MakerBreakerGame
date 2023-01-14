from typing import List

import arcade

from app.game.components.star_expansion import Star
from app.game.engine.interface import MovableObject
from app.game.engine.types import Point2D
from app.game.engine.utils import distance, offset, midpoint, get_quadratic_bezier_points, diff


class Edge(MovableObject):
    def __init__(self, points: List[Point2D], node_radius):
        self.points = points
        self.node_radius = node_radius

    def draw(self):
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
            star.draw(self.node_radius)

    def _draw2d(self, p0: Point2D, p2: Point2D, color=arcade.csscolor.WHITE, width=2):
        dist = distance(p0, p2)
        off = offset(dist)
        mid = midpoint(p0, p2)
        p1 = Point2D(mid.x + off, mid.y + off)
        points = get_quadratic_bezier_points(p0, p1, p2)
        arcade.draw_commands.draw_line_strip(points, color, width)

    def update(self, x: float, y: float):
        """Move an object to its new position"""
        diff_x, diff_y = diff(self.x, self.y, x, y)

        self.x += diff_x
        self.y += diff_y
