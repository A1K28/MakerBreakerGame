import math
from typing import List

from app.game.components.hyperedge import HyperEdge
from app.game.components.node import Node
from app.game.config.constants import Constants
from app.game.engine.types import Point2D
from app.game.engine.utils import get_distributed_points, distance, coulomb_attract, diff


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

    def pre_self_adjust(self):
        """Use a Force-Directed graph drawing algorithm,
         as Described at https://en.wikipedia.org/wiki/Force-directed_graph_drawing"""
        for i in range(int(1e4)):
            self.self_adjust()

    def self_adjust(self):
        """Use a Force-Directed graph drawing algorithm, used for visualisation purposes.
         as Described at https://en.wikipedia.org/wiki/Force-directed_graph_drawing"""
        self._apply_hooke_on_edges()
        self._apply_coulomb_on_nodes()

    def _apply_hooke_on_edges(self):
        for edge in self.edges:
            edge.update_with_hooke()

    def _apply_coulomb_on_nodes(self):
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                if i == j:
                    continue
                dist = distance(self.nodes[i].to_point(), self.nodes[j].to_point())
                force = coulomb_attract(dist)
                dx, dy = diff(self.nodes[i].point_x, self.nodes[i].point_y,
                              self.nodes[j].point_x, self.nodes[j].point_y)
                unit_x, unit_y = dx*1./dist, dy*1./dist
                dx, dy = unit_x*force, unit_y*force
                self.nodes[i].apply_force(-dx, -dy)

    def find_closest_node(self, x, y, threshold=30) -> Node | None:
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
