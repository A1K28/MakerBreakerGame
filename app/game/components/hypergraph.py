import math
from typing import List

from app.game.components.hyperedge import HyperEdge
from app.game.components.node import Node
from app.game.config.constants import Constants
from app.game.engine.types import Point2D
from app.game.engine.utils import get_distributed_points, distance


class HyperGraph:
    def __init__(self, width=1280, height=720, node_radius=12, font_size=10):
        self.width = width
        self.height = height
        self.node_radius = node_radius
        self.font_size = font_size
        # self.grid_visited = [[0] * self.grid_height] * self.grid_width

        self.nodes: List[Node] = []
        self.edges: List[HyperEdge] = []

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

    def create_edge(self, nodes: List[Node]):
        edge = HyperEdge(nodes, self.node_radius)
        self.edges.append(edge)

    def create_node(self, point, tag):
        node = Node(point, tag, self.node_radius, self.font_size)
        self.nodes.append(node)

    def draw_graph(self):
        # draw edges
        for edge in self.edges:
            edge.draw()

        # draw nodes
        for node in self.nodes:
            node.draw()

    def find_closest_node(self, x, y, threshold=10) -> Node | None:
        """Find the closes node that is not further than threshold (in pixels) from the given coordinates"""
        n = None
        dist = Constants.INFINITY
        point = Point2D(x, y)
        for node in self.nodes:
            new_dist = distance(point, node.to_point())
            if new_dist < dist:
                n = node
                dist = new_dist

        if dist <= threshold:
            return n
        return None
