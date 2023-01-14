import arcade

from app.game.engine.interface import MovableObject
from app.game.engine.types import Point2D
from app.game.engine.utils import diff


class Node(MovableObject):
    def __init__(self, point: Point2D, tag: str, radius: float, font_size: int):
        # self.point = point
        self.tag = tag
        self.radius = radius
        self.font_size = font_size

        self.point_x = point.x
        self.point_y = point.y

        self.text_x = self.point_x - self.radius / 2 + 2
        self.text_y = self.point_y - self.radius / 2 + 2
        if len(self.tag) == 2:
            self.font_size -= 2
            self.text_x -= 2

    def to_point(self) -> Point2D:
        return Point2D(self.point_x, self.point_y)

    def draw(self):
        """Draw the object to screen"""
        if len(self.tag) > 2:
            raise ValueError(f"Tag ({self.tag}) length is greater than 2")
        arcade.draw_circle_filled(self.point_x, self.point_y, self.radius, arcade.csscolor.ORANGE)
        arcade.draw_text(self.tag, self.text_x, self.text_y, font_size=self.font_size, color=arcade.csscolor.BLACK)

    def update(self, x: float, y: float):
        """Move an object to its new position"""
        circle_diff_x, circle_diff_y = diff(self.point_x, self.point_y, x, y)
        text_diff_x, text_diff_y = diff(self.text_x, self.text_y, x, y)

        self.point_x += circle_diff_x
        self.point_y += circle_diff_y
        self.text_x += text_diff_x
        self.text_y += text_diff_y
