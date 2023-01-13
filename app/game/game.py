import math
import random
from typing import List

import arcade

from app.game.components.edge import Edge
from app.game.components.node import Node
from app.game.config.constants import Constants
from app.game.config.types import Point2D
from app.game.engine.hypergraph import test_hypergraph


class MakerBreakerGame:
    def __init__(self, width=1280, height=720, node_radius=12, font_size=10):
        self.width = width
        self.height = height
        self.node_radius = node_radius
        self.font_size = font_size

        self.node_width = node_radius * 2 + 3
        self.grid_width = math.floor(width / self.node_width)
        self.grid_height = math.floor(height / self.node_width)
        self.grid_visited = [[0] * self.grid_height] * self.grid_width

        self.nodes: List[Node] = []
        self.edges: List[Edge] = []

    def get_grid_coords(self, p: Point2D) -> (int, int):
        return math.ceil(p.x / self.node_width), math.ceil(p.y / self.node_width)

    def get_distributed_points(self, n_points: int):
        # generate unique grid coords
        constraint_x = 25
        constraint_y = 16
        center_x = constraint_x*1./2*self.node_width
        center_y = constraint_y*1./2*self.node_width
        x_diff = self.width*1./2 - center_x
        y_diff = self.height*1./2 - center_y
        print(x_diff, y_diff)
        # arcade.draw_xywh_rectangle_outline(0, 0, constraint_x * self.node_width, constraint_y * self.node_width,
        #                                    arcade.csscolor.BLACK)
        # arcade.draw_xywh_rectangle_outline(self.width * 1. / 2 - center_x,
        #                                    self.height * 1. / 2 - center_y,
        #                                    constraint_x * self.node_width,
        #                                    constraint_y * self.node_width,
        #                                    arcade.csscolor.BLACK)
        random_points_1d = random.sample(range(0, constraint_x * constraint_y), n_points)
        print(random_points_1d)
        random_points = [Point2D(e % constraint_x * 1. * self.node_width + self.width * 1. / 2 - center_x,
                                 e / constraint_x * 1. * self.node_width + self.height * 1. / 2 - center_y)
                         for e in random_points_1d]
        return random_points

    def draw_graph(self, nodes, edges):
        # create nodes
        node_points = self.get_distributed_points(len(nodes))
        for np, tag in zip(node_points, nodes):
            self.create_node(np, tag)

        # create edges
        for edge in edges:
            nodes = [e for e in self.nodes if e.tag in edge]
            self.create_edge(nodes)

        # draw edges
        for edge in self.edges:
            edge.draw(self.node_radius)

        # draw nodes
        for node in self.nodes:
            node.draw()

    def create_edge(self, nodes: List[Node]):
        points = [e.point for e in nodes]
        edge = Edge(points)
        self.edges.append(edge)

    def create_node(self, point, tag):
        node = Node(point, tag, self.node_radius, self.font_size)
        self.nodes.append(node)

    def run(self):
        arcade.open_window(self.width, self.height, "Maker Breaker Game")

        arcade.set_background_color(Constants.DARK_BLUE_COLOR)

        arcade.start_render()

        self.draw_graph(nodes=test_hypergraph['nodes'], edges=test_hypergraph['edges'])

        arcade.finish_render()

        arcade.run()


if __name__ == '__main__':
    game = MakerBreakerGame()
    game.run()
