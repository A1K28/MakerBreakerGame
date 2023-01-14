import arcade

from app.game.engine.types import Point2D
from app.game.engine.utils import diff
from app.game.config.constants import Constants
from app.game.engine.interface import MovableObject, PhysicsObject


class Star(MovableObject, PhysicsObject):
    def __init__(self, x, y, node_radius, inner_radius):
        self.point_x = x
        self.point_y = y
        self.node_radius = node_radius
        self.inner_radius = inner_radius

    def draw(self):
        arcade.draw_circle_filled(self.point_x, self.point_y, self.node_radius, Constants.DARK_BLUE_COLOR)
        arcade.draw_circle_filled(self.point_x, self.point_y, self.inner_radius, arcade.csscolor.TOMATO)

    def update(self, x: float, y: float):
        """Move an object to its new position"""
        diff_x, diff_y = diff(self.point_x, self.point_y, x, y)

        self.point_x += diff_x
        self.point_y += diff_y

    def to_point(self) -> Point2D:
        return Point2D(self.point_x, self.point_y)

    def apply_force(self, f_x: float, f_y: float):
        self.point_x = max(self.node_radius, min(self.point_x + f_x, Constants.WIDTH - self.node_radius))
        self.point_y = max(self.node_radius, min(self.point_y + f_y, Constants.HEIGHT - self.node_radius))
