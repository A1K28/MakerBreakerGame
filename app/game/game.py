# import sys
# sys.path.append('/Users/ak/PycharmProjects/MakerBreakerGame')

import arcade

from app.game.components.hypergraph import HyperGraph
from app.game.config.constants import Constants
from app.game.engine.data import test_hypergraph
from app.game.engine.interface import SelectableObject, PhysicsObject


class MakerBreakerGame(arcade.Window):
    def __init__(self, node_radius=12, font_size=10, pre_adjust=False):
        super().__init__(Constants.WIDTH, Constants.HEIGHT, title="Maker Breaker Game")

        self.hypergraph = HyperGraph(Constants.WIDTH, Constants.HEIGHT, node_radius, font_size)
        self.right_mouse_bound_object: PhysicsObject | None = None
        self.hover_bound_object: SelectableObject | PhysicsObject | None = None

        self.pre_adjust = pre_adjust
        self.setup()

    def setup(self):
        arcade.set_background_color(Constants.DARK_BLUE_COLOR)
        self.hypergraph.create_graph(nodes=test_hypergraph['nodes'], edges=test_hypergraph['edges'])
        if self.pre_adjust:
            self.hypergraph.pre_self_adjust()

    def on_draw(self):
        arcade.start_render()
        self.hypergraph.draw_graph()
        if self.hover_bound_object is not None and self.right_mouse_bound_object is None:
            self.hypergraph.draw_color_palette()
            self.hypergraph.update_color_palette(self.hover_bound_object.point_x,
                                                 self.hover_bound_object.point_y)

        if self.right_mouse_bound_object is not None:
            self.right_mouse_bound_object.update()

        self.hypergraph.self_adjust()
        self.hypergraph.self_center()

    def on_mouse_motion(self, x, y, dx, dy):
        """Called when the mouse moves."""
        # handle mouse bound object
        if self.right_mouse_bound_object is not None:
            self._set_velocity_to_right_mouse_bound_object(x, y)

        # handle on-hover
        if self.right_mouse_bound_object is not None:
            self.hover_bound_object = self.right_mouse_bound_object
        elif not (self.hover_bound_object is not None and self.hypergraph.is_point_on_color_palette(x, y)):
            node = self.hypergraph.find_closest_node(x, y)
            if self.hover_bound_object is not None and node != self.hover_bound_object:
                self._clear_node_color()

            if node is not None and node != self.hover_bound_object:
                self._set_node_color(node)

    def on_mouse_press(self, x, y, button, modifiers):
        """Called when the mouse is pressed"""
        # left mouse button. pick a color.
        # if button == 1:
        #     print("HERE")

        # right mouse button. move an object.
        if button == 4:
            if self.right_mouse_bound_object is None:
                node = self.hypergraph.find_closest_node(x, y)
                if node is not None:
                    node.vel_x = x
                    node.vel_y = y
                    self.right_mouse_bound_object = node
                    self.right_mouse_bound_object.select()
            else:
                self.right_mouse_bound_object.deselect()
                self.right_mouse_bound_object = None
                self._clear_node_color()
                self.hover_bound_object = None

    # def on_mouse_release(self, x, y, button, modifiers):
    #     """Called when the mouse is released"""
    #     if button == 1:
    #         self.mouse_bound_object = None

    def _set_velocity_to_right_mouse_bound_object(self, vel_x, vel_y):
        self.right_mouse_bound_object.vel_x = vel_x
        self.right_mouse_bound_object.vel_y = vel_y

    def _set_position_to_color_palette(self, x, y):
        self.hypergraph.color_palette.point_x = x
        self.hypergraph.color_palette.point_y = y

    def _clear_node_color(self):
        self.hover_bound_object.color = self.hover_bound_object.default_color
        for edge in self.hypergraph.get_edges(self.hover_bound_object):
            edge.color = edge.default_color
        self.hover_bound_object = None

    def _set_node_color(self, node):
        self.hover_bound_object = node
        self.hover_bound_object.color = arcade.csscolor.ROYAL_BLUE
        for edge in self.hypergraph.get_edges(self.hover_bound_object):
            edge.color = arcade.csscolor.VIOLET
        self._set_position_to_color_palette(node.point_x, node.point_y)


if __name__ == '__main__':
    game = MakerBreakerGame()
    arcade.run()
