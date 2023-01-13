import arcade

from app.game.config.constants import Constants


class Star:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, node_radius):
        arcade.draw_circle_filled(self.x, self.y, node_radius, Constants.DARK_BLUE_COLOR)
        arcade.draw_circle_filled(self.x, self.y, self.radius, arcade.csscolor.TOMATO)
