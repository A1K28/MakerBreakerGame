# import sys
# sys.path.append('/Users/ak/PycharmProjects/MakerBreakerGame')

import arcade

from app.game.components.hypergraph import HyperGraph
from app.game.config.constants import Constants
from app.game.engine.data import test_hypergraph
from app.game.engine.interface import MovableObject, SelectableObject


class MakerBreakerGame(arcade.Window):
    def __init__(self, node_radius=12, font_size=10):
        super().__init__(Constants.WIDTH, Constants.HEIGHT, title="Maker Breaker Game")

        self.hypergraph = HyperGraph(Constants.WIDTH, Constants.HEIGHT, node_radius, font_size)
        self.mouse_bound_object: MovableObject | None = None
        self.hover_bound_object: SelectableObject | None = None

        self.setup()


    def setup(self):
        arcade.set_background_color(Constants.DARK_BLUE_COLOR)
        self.hypergraph.create_graph(nodes=test_hypergraph['nodes'], edges=test_hypergraph['edges'])
        # self.hypergraph.pre_self_adjust()

    def on_draw(self):
        arcade.start_render()
        self.hypergraph.draw_graph()
        self.hypergraph.self_adjust()
        self.hypergraph.self_center()

    def on_mouse_motion(self, x, y, dx, dy):
        """Called when the mouse moves."""
        # handle mouse bound object
        if self.mouse_bound_object is not None:
            self.mouse_bound_object.update(x, y)

        # handle on-hover
        node = self.hypergraph.find_closest_node(x, y)
        if self.hover_bound_object is not None:
            self.hover_bound_object.color = self.hover_bound_object.default_color
            for edge in self.hypergraph.get_edges(self.hover_bound_object):
                edge.color = edge.default_color

        if node is not None:
            self.hover_bound_object = node
            self.hover_bound_object.color = arcade.csscolor.ROYAL_BLUE
            for edge in self.hypergraph.get_edges(self.hover_bound_object):
                edge.color = arcade.csscolor.VIOLET

    def on_mouse_press(self, x, y, button, modifiers):
        """Called when the mouse is pressed"""
        if button == 4:
            if self.mouse_bound_object is None:
                node = self.hypergraph.find_closest_node(x, y)
                if node is not None:
                    self.mouse_bound_object = node
                    self.mouse_bound_object.select()
            else:
                self.mouse_bound_object.deselect()
                self.mouse_bound_object = None

    # def on_mouse_release(self, x, y, button, modifiers):
    #     """Called when the mouse is released"""
    #     if button == 1:
    #         self.mouse_bound_object = None


if __name__ == '__main__':
    game = MakerBreakerGame()
    arcade.run()
