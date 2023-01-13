import arcade

from app.game.config.types import Point2D


class Node:
    def __init__(self, point: Point2D, tag: str, radius: float, font_size: int):
        self.point = point
        self.tag = tag
        self.radius = radius
        self.font_size = font_size

    def draw(self):
        if len(self.tag) > 2:
            raise ValueError(f"Tag ({self.tag}) length is greater than 2")
        text_x = self.point.x - self.radius / 2 + 2
        text_y = self.point.y - self.radius / 2 + 2
        if len(self.tag) == 2:
            self.font_size -= 2
            text_x -= 2
        arcade.draw_circle_filled(self.point.x, self.point.y, self.radius, arcade.csscolor.ORANGE)
        arcade.draw_text(self.tag, text_x, text_y, font_size=self.font_size, color=arcade.csscolor.BLACK)
