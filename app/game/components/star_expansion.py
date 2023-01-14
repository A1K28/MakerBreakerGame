import arcade

from app.game.engine.utils import diff
from app.game.config.constants import Constants
from app.game.engine.interface import MovableObject


class Star(MovableObject):
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, node_radius):
        arcade.draw_circle_filled(self.x, self.y, node_radius, Constants.DARK_BLUE_COLOR)
        arcade.draw_circle_filled(self.x, self.y, self.radius, arcade.csscolor.TOMATO)

    def update(self, x: float, y: float):
        """Move an object to its new position"""
        diff_x, diff_y = diff(self.x, self.y, x, y)

        self.x += diff_x
        self.y += diff_y
