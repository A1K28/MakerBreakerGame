import arcade

from app.game.config.constants import Constants
from app.game.engine.interface import PhysicsObject, SelectableObject
from app.game.engine.types import Point2D
from app.game.engine.utils import diff, hypotenuse


class Node(PhysicsObject, SelectableObject):
    def __init__(self, point: Point2D, tag: str, radius: float, font_size: int):
        if len(tag) > 2:
            raise ValueError(f"Tag ({tag}) length is greater than 2")

        self.tag = tag
        self.radius = radius
        self.color = Constants.NODE_INNER_COLOR
        self.outer_color = Constants.NODE_OUTER_COLOR
        self.default_color = Constants.NODE_INNER_COLOR
        self.font_size = font_size

        self.is_selected: bool = False

        self.point_x = point.x
        self.point_y = point.y

        self.vel_x = 0
        self.vel_y = 0

        self.text_x = self.point_x - self.radius / 2 + 2
        self.text_y = self.point_y - self.radius / 2 + 2
        if len(self.tag) == 2:
            self.font_size -= 2
            self.text_x -= 2

    def draw(self):
        """Draw the object to screen"""
        arcade.draw_circle_filled(self.point_x, self.point_y, self.radius, self.outer_color)
        arcade.draw_circle_filled(self.point_x, self.point_y, self.radius-3, self.color)
        # arcade.draw_text(self.tag, self.text_x, self.text_y, font_size=self.font_size, color=arcade.csscolor.BLACK)

    def update(self):
        """Move an object to its new position"""
        circle_dx, circle_dy = diff(self.point_x, self.point_y, self.vel_x, self.vel_y)
        text_dx, text_dy = diff(self.text_x, self.text_y, self.vel_x, self.vel_y)

        dist = hypotenuse(circle_dx, circle_dy)
        if dist > 1:
            circle_dx *= Constants.DRAG_CONSTANT
            circle_dy *= Constants.DRAG_CONSTANT
            text_dx *= Constants.DRAG_CONSTANT
            text_dy *= Constants.DRAG_CONSTANT

        self._apply_force_on_point(circle_dx, circle_dy, True)
        self._apply_force_on_text(text_dx, text_dy, True)

    def apply_force(self, f_x: float, f_y: float):
        self._apply_force_on_point(f_x, f_y)
        self._apply_force_on_text(f_x, f_y)

    def _apply_force_on_point(self, f_x: float, f_y: float, force: bool = False):
        if not self.is_selected or force:
            self.point_x = max(self.radius, min(self.point_x + f_x, Constants.WIDTH-self.radius))
            self.point_y = max(self.radius, min(self.point_y + f_y, Constants.HEIGHT-self.radius))

    def _apply_force_on_text(self, f_x: float, f_y: float, force: bool = False):
        if not self.is_selected or force:
            self.text_x = max(self.radius, min(self.text_x + f_x, Constants.WIDTH-self.radius))
            self.text_y = max(self.radius, min(self.text_y + f_y, Constants.HEIGHT-self.radius))
