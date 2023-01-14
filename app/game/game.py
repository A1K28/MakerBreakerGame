# import sys
# sys.path.append('/Users/ak/PycharmProjects/MakerBreakerGame')

import arcade

from app.game.components.hypergraph import HyperGraph
from app.game.config.constants import Constants
from app.game.engine.hypergraph import test_hypergraph
from app.game.engine.interface import MovableObject


class MakerBreakerGame(arcade.Window):
    def __init__(self, width=1280, height=720, node_radius=12, font_size=10):
        super().__init__(width, height, title="Maker Breaker Game")
        self.width = width
        self.height = height

        self.hypergraph = HyperGraph(width, height, node_radius, font_size)
        self.mouse_bound_object: MovableObject | None = None

        self.setup()

    def setup(self):
        arcade.set_background_color(Constants.DARK_BLUE_COLOR)
        self.hypergraph.create_graph(nodes=test_hypergraph['nodes'], edges=test_hypergraph['edges'])

    def on_draw(self):
        # pass
        arcade.start_render()

        self.hypergraph.draw_graph()
        # arcade.draw_circle_filled(self.x, self.y, 25, arcade.color.GREEN)
        # arcade.set_background_color(Constants.DARK_BLUE_COLOR)

        # arcade.open_window(self.width, self.height, "Maker Breaker Game")

        # arcade.start_render()

        # self.draw_graph(nodes=test_hypergraph['nodes'], edges=test_hypergraph['edges'])

        # arcade.finish_render()

        # arcade.run()

    # def on_mouse_motion(self, x, y, dx, dy):
    #     """Called when the mouse moves."""
    #     if self.mouse_bound_object is not None:
    #         self.mouse_bound_object.update(x, y)
    #
    # def on_mouse_press(self, x, y, button, modifiers):
    #     """Called when the mouse is pressed"""
    #     if button == 1:
    #         node = self.hypergraph.find_closest_node(x, y)
    #         if node is not None:
    #             self.mouse_bound_object = node
    #
    # def on_mouse_release(self, x, y, button, modifiers):
    #     """Called when the mouse is released"""
    #     if button == 1:
    #         self.mouse_bound_object = None


if __name__ == '__main__':
    game = MakerBreakerGame()
    arcade.run()
