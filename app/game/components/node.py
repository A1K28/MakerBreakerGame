import arcade

from app.game.config.constants import Constants
from app.game.engine.interface import MovableObject, PhysicsObject, SelectableObject
from app.game.engine.types import Point2D
from app.game.engine.utils import diff


class Node(MovableObject, SelectableObject, PhysicsObject):
    def __init__(self, point: Point2D, tag: str, radius: float, color: arcade.csscolor, font_size: int):
        # self.point = point
        self.tag = tag
        self.radius = radius
        self.color = color
        self.default_color = color
        self.font_size = font_size

        self.is_selected: bool = False

        self.point_x = point.x
        self.point_y = point.y

        self.text_x = self.point_x - self.radius / 2 + 2
        self.text_y = self.point_y - self.radius / 2 + 2
        if len(self.tag) == 2:
            self.font_size -= 2
            self.text_x -= 2

    def draw(self):
        """Draw the object to screen"""
        if len(self.tag) > 2:
            raise ValueError(f"Tag ({self.tag}) length is greater than 2")
        arcade.draw_circle_filled(self.point_x, self.point_y, self.radius, Constants.DARK_BLUE_COLOR)
        arcade.draw_circle_filled(self.point_x, self.point_y, self.radius-3, self.color)
        # arcade.draw_text(self.tag, self.text_x, self.text_y, font_size=self.font_size, color=arcade.csscolor.BLACK)

    def select(self):
        """Selects an object"""
        self.is_selected = True

    def deselect(self):
        """Deselects an object"""
        self.is_selected = False

    def update(self, x: float, y: float):
        """Move an object to its new position"""
        circle_diff_x, circle_diff_y = diff(self.point_x, self.point_y, x, y)
        text_diff_x, text_diff_y = diff(self.text_x, self.text_y, x, y)

        self._apply_force_on_point(circle_diff_x, circle_diff_y, True)
        self._apply_force_on_text(text_diff_x, text_diff_y, True)

    def to_point(self) -> Point2D:
        return Point2D(self.point_x, self.point_y)

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
