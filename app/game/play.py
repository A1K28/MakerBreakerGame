import math
from typing import List

import arcade

from app.service.hypergraph import decompose_edges_by_len, test_hypergraph
from app.game.types import Point2D


def distance(p1: Point2D, p2: Point2D) -> float:
    return math.sqrt(abs(p1.x - p2.x) ** 2 + abs(p1.y - p2.y) ** 2)


def slope(p1: Point2D, p2: Point2D) -> float:
    return abs(p1.y - p2.y) * 1. / abs(p1.x - p2.x)


def midpoint(p1: Point2D, p2: Point2D) -> Point2D:
    return Point2D((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)


def find_center_of_circle(p1: Point2D, p2: Point2D, k=2) -> Point2D:
    """
    Since the arcade library does not offer Bezier Curves, we must improvise.
    Therefore, we draw an arc, and pass it off as a nice curve to connect 2 nodes.

    How to draw:
    Let d be the distance between the two given points.
    Let k be some constant that determines the radius, defined as r/d=k.
    Let m be the slope of the line between the two given points.

    Let m' be the slope of the orthogonal line from the line that connects the two points (thus, m' = -1/m).
    Let mid be the midpoint of the two given points.
    Let r be the distance between the mid-point and the center of the circle - O.
    Let r_x & r_y be the components (cathetus) of the right triangle
        created by the midpoint & the center of the circle - O

    To find the point O, we write the following 2 equations:
    r_y/r_x = m'
    sqrt(r_x^2+r_y^2) = r

    which yields:
    r_x = sqrt(r^2/(1+m'^2))
    r_y = m'*r_x
    """
    dist = distance(p1, p2)
    m = slope(p1, p2)
    m_prime = -1. / m
    mid = midpoint(p1, p2)
    r = k * dist
    print(r)
    r_x = math.sqrt(r**2 / (1 + m_prime**2))
    r_y = m_prime * r_x
    print(r_x, r_y)
    r_point = Point2D(mid.x - r_x, mid.y - r_y)
    print(r_point)
    return r_point


def draw_quadratic_bezier(p0: Point2D, p1: Point2D, p2: Point2D, max_precision=128):
    """
    Formulated from https://en.wikipedia.org/wiki/B%C3%A9zier_curve#Quadratic_B%C3%A9zier_curves.

    A quadratic Bézier curve is the path traced by B(t) given points p0, p1 & p2.
    Where parameter t describes how far B(t) is from p0 to p2 (the endpoints).

    B(t) = (1-t)^2*P0 + 2(1-t)t*P1 + t^2*P2
    """
    def b(t: float) -> Point2D:
        c0 = (1-t)**2
        c1 = 2*(1-t)*t
        c2 = t**2
        p0_m = Point2D(c0*p0.x, c0*p0.y)
        p1_m = Point2D(c1*p1.x, c1*p1.y)
        p2_m = Point2D(c2*p2.x, c2*p2.y)
        return Point2D(p0_m.x + p1_m.x + p2_m.x, p0_m.y + p1_m.y + p2_m.y)

    dist = distance(p0, p2)
    precision = max(12, min(max_precision, int(dist * 0.25)))

    points = []
    for i in range(precision + 1):
        t0 = min(1., 1. * i / precision)
        p = b(t0)
        points.append(p)

    arcade.draw_commands.draw_line_strip(points, arcade.csscolor.WHITE, 1.1)


offset = lambda x: 1./28*x+10./7


def draw_edge(p0: Point2D, p2: Point2D):
    dist = distance(p0, p2)
    off = offset(dist)
    mid = midpoint(p0, p2)
    p1 = Point2D(mid.x+off, mid.y+off)
    draw_quadratic_bezier(p0, p1, p2)


def draw_point(p: Point2D, color=arcade.csscolor.WHITE):
    arcade.draw_point(p.x, p.y, color=color, size=10)


def draw_points(points: List[Point2D]):
    for point in points:
        draw_point(point)


def draw_graph(nodes, edges):
    # draw nodes in circle
    mid_x = 1280 / 2
    mid_y = 720 / 2
    radii = 2 * len(nodes) + 100
    fi = 0
    step = 360 * 1. / len(nodes)
    node_points = []
    for i, node in enumerate(nodes):
        x = math.cos(math.radians(fi)) * radii
        y = math.sin(math.radians(fi)) * radii
        np = Point2D(mid_x + x, mid_y + y)
        node_points.append(np)
        fi = (fi + step) % 360

    # connect i & i+1 nodes
    for i in range(len(node_points)):
        draw_edge(node_points[i], node_points[(i+1) % len(node_points)])

    for i, np in enumerate(node_points):
        draw_node(np.x, np.y, str(i + 1))



def draw_node(x, y, tag, radius=12, font_size=10):
    if len(tag) > 2:
        raise ValueError(f"Tag ({tag}) length is greater than 2")
    text_x = x - radius / 2 + 2
    text_y = y - radius / 2 + 2
    if len(tag) == 2:
        font_size -= 2
        text_x -= 2
    arcade.draw_circle_filled(x, y, radius, arcade.csscolor.ORANGE)
    arcade.draw_text(tag, text_x, text_y, font_size=font_size, color=arcade.csscolor.BLACK)


class MakerBreakerGame:
    DARK_BLUE_COLOR = (0, 48, 73)

    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height

    def run(self):
        arcade.open_window(self.width, self.height, "Drawing Example")

        arcade.set_background_color(self.DARK_BLUE_COLOR)

        arcade.start_render()

        draw_graph(nodes=test_hypergraph['nodes'], edges=decompose_edges_by_len(test_hypergraph['edges']))

        arcade.finish_render()

        arcade.run()


if __name__ == '__main__':
    game = MakerBreakerGame()
    game.run()
