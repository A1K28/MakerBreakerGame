import math

import arcade

from app.game.config.constants import Constants
from app.game.engine.interface import PhysicsObject
from app.game.engine.utils import diff, is_point_inside_rect, hypotenuse


class ColorPalette(PhysicsObject):
    def __init__(self, x, y, node_radius, padding: float = 5, margin: float = 2):
        self.point_x = x
        self.point_y = y
        self.vel_x = 0
        self.vel_y = 0
        self.node_radius = node_radius
        self.padding = padding
        self.margin = margin
        self.colors = Constants.COLOR_PALETTE_LIST
        self.width = self.node_radius * 2. * len(self.colors) + self.padding * (len(self.colors) + 1)
        self.height = self.node_radius * 2. + self.padding * 2

    def draw(self):
        rect_x, rect_y = self._get_xy()
        arcade.draw_xywh_rectangle_filled(
            rect_x, rect_y, self.width, self.height, Constants.BACKGROUND_COLOR)

        w, h = self.node_radius*2, self.node_radius*2
        for i, color in enumerate(self.colors):
            pad_left = i*self.node_radius*2 + i*self.padding + self.padding
            arcade.draw_xywh_rectangle_filled(
                rect_x + pad_left, rect_y + self.padding, w, h, color)

    def update(self):
        """Move an object to its new position"""
        dx, dy = diff(self.point_x, self.point_y, self.vel_x, self.vel_y)
        dist = hypotenuse(dx, dy)
        if dist > 1:
            dx *= Constants.DRAG_CONSTANT
            dy *= Constants.DRAG_CONSTANT
        self.apply_force(dx, dy)

    def apply_force(self, f_x: float, f_y: float):
        """Apply the given force to an object"""
        self.point_x = max(self.node_radius, min(self.point_x + f_x, Constants.WIDTH - self.node_radius))
        self.point_y = max(self.node_radius, min(self.point_y + f_y, Constants.HEIGHT - self.node_radius))

    def is_point_inside_palette(self, x, y) -> bool:
        rect_x, rect_y = self._get_xy()
        return is_point_inside_rect(x, y, rect_x, rect_y, self.width, self.height)

    def set_colors(self, colors):
        self.colors = colors
        self.width = self.node_radius * 2. * len(self.colors) + self.padding * (len(self.colors) + 1)

    def get_color_from_pos(self, x, y) -> arcade.csscolor:
        rect_x, rect_y = self._get_xy()
        if is_point_inside_rect(x, y, rect_x, rect_y, self.width, self.height, threshold=0):
            dx = x - rect_x
            block_width = self.width*1./len(self.colors)
            return self.colors[math.floor(dx*1. / block_width)]
        return None

    def _get_xy(self) -> (float, float):
        """Returns the X & Y coordinates of the rectangle from the bottom left"""
        return self.point_x - self.width*1./2, self.point_y + self.node_radius + self.margin
