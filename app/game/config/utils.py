import math

import arcade

from app.game.config.types import Point2D


offset = lambda x: 2.5 / 28 * x + 10./7


def distance(p1: Point2D, p2: Point2D) -> float:
    return math.sqrt(abs(p1.x - p2.x) ** 2 + abs(p1.y - p2.y) ** 2)


def slope(p1: Point2D, p2: Point2D) -> float:
    return abs(p1.y - p2.y) * 1. / abs(p1.x - p2.x)


def midpoint(p1: Point2D, p2: Point2D) -> Point2D:
    return Point2D((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)


def draw_quadratic_bezier(p0: Point2D, p1: Point2D, p2: Point2D,
                          max_precision=128, color=arcade.csscolor.WHITE, width=2):
    """
    Formulated from https://en.wikipedia.org/wiki/B%C3%A9zier_curve#Quadratic_B%C3%A9zier_curves.

    A quadratic Bézier curve is the path traced by B(t) given points p0, p1 & p2.
    Where parameter t describes how far B(t) is from p0 to p2 (the endpoints).

    B(t) = (1-t)^2*P0 + 2(1-t)t*P1 + t^2*P2
    """

    def b(t: float) -> Point2D:
        c0 = (1 - t) ** 2
        c1 = 2 * (1 - t) * t
        c2 = t ** 2
        p0_m = Point2D(c0 * p0.x, c0 * p0.y)
        p1_m = Point2D(c1 * p1.x, c1 * p1.y)
        p2_m = Point2D(c2 * p2.x, c2 * p2.y)
        return Point2D(p0_m.x + p1_m.x + p2_m.x, p0_m.y + p1_m.y + p2_m.y)

    dist = distance(p0, p2)
    precision = max(12, min(max_precision, int(dist * 0.25)))

    points = []
    for i in range(precision + 1):
        t0 = min(1., 1. * i / precision)
        p = b(t0)
        points.append(p)

    arcade.draw_commands.draw_line_strip(points, color, width)
