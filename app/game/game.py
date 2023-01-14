import math
from typing import List

import arcade

from app.game.components.edge import Edge
from app.game.components.node import Node
from app.game.config.constants import Constants
from app.game.engine.hypergraph import test_hypergraph
from app.game.engine.types import Point2D
from app.game.engine.utils import get_distributed_points


class MakerBreakerGame(arcade.Window):
    def __init__(self, width=1280, height=720, node_radius=12, font_size=10):
        super().__init__(width, height, title="Maker Breaker Game")

        self.width = width
        self.height = height
        self.node_radius = node_radius
        self.font_size = font_size
        # self.grid_visited = [[0] * self.grid_height] * self.grid_width

        self.nodes: List[Node] = []
        self.edges: List[Edge] = []

        self.setup()

    def setup(self):
        arcade.set_background_color(Constants.DARK_BLUE_COLOR)
        self.create_graph(nodes=test_hypergraph['nodes'], edges=test_hypergraph['edges'])

    def create_graph(self, nodes, edges):
        # get random unique node points
        node_width = self.node_radius * 2 + 3
        grid_width = math.floor(self.width / node_width)
        grid_height = math.floor(self.height / node_width)
        node_points = get_distributed_points(self.width, self.height, node_width, len(nodes))

        # create nodes
        for np, tag in zip(node_points, nodes):
            self.create_node(np, tag)

        # create edges
        for edge in edges:
            nodes = [e for e in self.nodes if e.tag in edge]
            self.create_edge(nodes)

    def draw_graph(self):
        # draw edges
        for edge in self.edges:
            edge.draw()

        # draw nodes
        for node in self.nodes:
            node.draw()

    def create_edge(self, nodes: List[Node]):
        points = [Point2D(e.point_x, e.point_y) for e in nodes]
        edge = Edge(points, self.node_radius)
        self.edges.append(edge)

    def create_node(self, point, tag):
        node = Node(point, tag, self.node_radius, self.font_size)
        self.nodes.append(node)

    def on_draw(self):
        # pass
        arcade.start_render()

        self.draw_graph()
        # arcade.draw_circle_filled(self.x, self.y, 25, arcade.color.GREEN)
        # arcade.set_background_color(Constants.DARK_BLUE_COLOR)

        # arcade.open_window(self.width, self.height, "Maker Breaker Game")

        # arcade.start_render()

        # self.draw_graph(nodes=test_hypergraph['nodes'], edges=test_hypergraph['edges'])

        # arcade.finish_render()

        # arcade.run()

    # Creating function to check the position
    # of the mouse
    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        self.nodes[0].update(x, y)

    # Creating function to check the mouse clicks
    def on_mouse_press(self, x, y, button, modifiers):
        print("Mouse button is pressed")


if __name__ == '__main__':
    game = MakerBreakerGame()
    arcade.run()
