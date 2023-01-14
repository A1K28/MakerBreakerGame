from typing import List

import arcade

from app.game.components.node import Node
from app.game.components.star_expansion import Star
from app.game.config.constants import Constants
from app.game.engine.types import Point2D
from app.game.engine.utils import distance, offset, midpoint, get_quadratic_bezier_points, diff


class HyperEdge:
    def __init__(self, nodes: List[Node], node_radius: float, color: arcade.csscolor):
        self.nodes = nodes
        self.node_radius = node_radius
        self.color = color
        self.default_color = color

        # star expansion (for edges with more than 2 endpoints)
        self.star: Star | None = None

    def draw(self):
        if self.nodes is None or len(self.nodes) < 2:
            raise ValueError(f"Invalid point array passed ar argument: {self.nodes}")
        elif len(self.nodes) == 2:
            n0, n2 = self.nodes[0], self.nodes[1]
            self._draw2d(n0.to_point(), n2.to_point(), self.color)
        else:
            mid = self.nodes[0].to_point()
            for i in range(1, len(self.nodes)):
                mid = midpoint(mid, self.nodes[i].to_point())
            for node in self.nodes:
                self._draw2d(node.to_point(), mid, self.color)
            self.star = Star(mid.x, mid.y, self.node_radius, 6)
            self.star.draw()

    @staticmethod
    def _draw2d(p0: Point2D, p2: Point2D, color=arcade.csscolor.WHITE, width=2):
        dist = distance(p0, p2)
        off = offset(dist)
        mid = midpoint(p0, p2)
        p1 = Point2D(mid.x + off, mid.y + off)
        points = get_quadratic_bezier_points(p0, p1, p2)
        arcade.draw_commands.draw_line_strip(points, color, width)

    def update_with_hooke(self):
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                if i == j:
                    continue
                dx, dy = diff(self.nodes[i].point_x, self.nodes[i].point_y,
                              self.nodes[j].point_x, self.nodes[j].point_y)

                # F = kx
                force_x, force_y = Constants.HOOKE_K * dx, Constants.HOOKE_K * dy
                self.nodes[i].apply_force(force_x, force_y)
