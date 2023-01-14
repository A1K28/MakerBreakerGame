import math
import random
from typing import List

from app.game.engine.types import Point2D


def offset(dist: float) -> float:
    return 2.5 / 28 * dist + 10./7


def distance(p1: Point2D, p2: Point2D) -> float:
    """Find distance between two points on an Euclidian plane"""
    return math.sqrt(abs(p1.x - p2.x) ** 2 + abs(p1.y - p2.y) ** 2)


def slope(p1: Point2D, p2: Point2D) -> float:
    """Find slope between two points an Euclidian plane"""
    return abs(p1.y - p2.y) * 1. / abs(p1.x - p2.x)


def midpoint(p1: Point2D, p2: Point2D) -> Point2D:
    """Find midpoint between two points on an Euclidian plane."""
    return Point2D((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)


def diff(old_x: float, old_y: float, new_x: float, new_y: float) -> (float, float):
    """Find difference vector between two points on an Euclidian plane"""
    return new_x-old_x, new_y-old_y


def get_quadratic_bezier_points(p0: Point2D, p1: Point2D, p2: Point2D, max_precision=128) -> List[Point2D]:
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
    return points


def get_distributed_points(width: int, height: int, block_size: int, n_points: int,
                           grid_width: int = 25, grid_height: int = 16):
    """Returns a list of N unique points uniformly distributed along the grid"""
    # generate unique grid coords
    constraint_x = grid_width
    constraint_y = grid_height
    center_x = constraint_x*1./2*block_size
    center_y = constraint_y*1./2*block_size
    x_diff = width*1./2 - center_x
    y_diff = height*1./2 - center_y
    # arcade.draw_xywh_rectangle_outline(0, 0, constraint_x * self.node_width, constraint_y * self.node_width,
    #                                    arcade.csscolor.BLACK)
    # arcade.draw_xywh_rectangle_outline(self.width * 1. / 2 - center_x,
    #                                    self.height * 1. / 2 - center_y,
    #                                    constraint_x * self.node_width,
    #                                    constraint_y * self.node_width,
    #                                    arcade.csscolor.BLACK)
    random_points_1d = random.sample(range(0, constraint_x * constraint_y), n_points)
    random_points = [Point2D(e % constraint_x * 1. * block_size + width * 1. / 2 - center_x,
                             e / constraint_x * 1. * block_size + height * 1. / 2 - center_y)
                     for e in random_points_1d]
    return random_points
