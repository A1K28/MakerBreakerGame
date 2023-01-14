import math
from typing import List, Dict

import arcade

from app.game.components.hyperedge import HyperEdge
from app.game.components.node import Node
from app.game.config.constants import Constants
from app.game.engine.types import Point2D
from app.game.engine.utils import get_distributed_points, distance, coulomb_attract, diff, hypotenuse


class HyperGraph:
    def __init__(self, width=1280, height=720, node_radius=12, font_size=10):
        self.width = width
        self.height = height
        self.node_radius = node_radius
        self.font_size = font_size
        # self.grid_visited = [[0] * self.grid_height] * self.grid_width

        self.nodes: List[Node] = []
        self.edges: List[HyperEdge] = []
        self.node_edge_map: Dict[str, List[HyperEdge]] = {}

    def create_graph(self, nodes, edges):
        # get random unique node points
        node_width = self.node_radius * 2 + 3
        grid_width = math.floor(self.width / node_width)
        grid_height = math.floor(self.height / node_width)
        node_points = get_distributed_points(self.width, self.height, node_width, len(nodes))

        # create nodes
        for np, tag in zip(node_points, nodes):
            self._create_node(np, tag)

        # create edges
        for edge in edges:
            nodes = [e for e in self.nodes if e.tag in edge]
            self._create_edge(nodes)

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
        for i in range(int(1e3)):
            self.self_adjust()
            self.self_center()

    def self_adjust(self):
        """Use a Force-Directed graph drawing algorithm, used for visualisation purposes.
         as Described at https://en.wikipedia.org/wiki/Force-directed_graph_drawing"""
        self._apply_hooke_on_edges()
        self._apply_coulomb_on_nodes()

    def self_center(self):
        x, y, w, h = self._get_rectangle_xywh_containing_all_nodes()
        x_hat = Constants.WIDTH*1./2-(2*x+w)*1./2
        y_hat = Constants.HEIGHT*1./2-(2*y+h)*1./2
        magnitude = 1000./math.log(hypotenuse(x_hat, y_hat))
        dx, dy = x_hat*1./magnitude, y_hat*1./magnitude
        for node in self.nodes:
            node.apply_force(dx, dy)

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

    def get_edges(self, node) -> List[HyperEdge]:
        return self.node_edge_map[node.tag]

    def _create_edge(self, nodes: List[Node]):
        edge = HyperEdge(nodes, self.node_radius, arcade.csscolor.WHITE)
        self.edges.append(edge)
        for node in nodes:
            if node.tag not in self.node_edge_map:
                self.node_edge_map[node.tag] = []
            self.node_edge_map[node.tag].append(edge)

    def _create_node(self, point, tag):
        node = Node(point, tag, self.node_radius, arcade.csscolor.ORANGE, self.font_size)
        self.nodes.append(node)

    def _get_rectangle_xywh_containing_all_nodes(self) -> (float, float, float, float):
        # defined vars
        outer_left = Constants.WIDTH
        outer_right = 0
        outer_bottom = Constants.HEIGHT
        outer_top = 0

        # find minimums and maximums
        for node in self.nodes:
            if node.point_x < outer_left:
                outer_left = node.point_x
            if node.point_x > outer_right:
                outer_right = node.point_x
            if node.point_y < outer_bottom:
                outer_bottom = node.point_y
            if node.point_y > outer_top:
                outer_top = node.point_y

        # heads up! trying to be careful
        if outer_right == outer_right:
            outer_left -= self.node_radius
            outer_right += self.node_radius
        if outer_top == outer_bottom:
            outer_bottom -= self.node_radius
            outer_top += self.node_radius

        # return x, y from the bottom left, along with width and height
        x, y = outer_left-self.node_radius, outer_bottom-self.node_radius
        w, h = outer_right-outer_left+2*self.node_radius, outer_top-outer_bottom+2*self.node_radius
        return x, y, w, h

    def _apply_hooke_on_edges(self):
        for edge in self.edges:
            edge.update_with_hooke()

    def _apply_coulomb_on_nodes(self):
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                if i == j:
                    continue
                dist = distance(self.nodes[i].to_point(), self.nodes[j].to_point())
                if dist == 0:
                    dist = self.node_radius
                force = coulomb_attract(dist)
                dx, dy = diff(self.nodes[i].point_x, self.nodes[i].point_y,
                              self.nodes[j].point_x, self.nodes[j].point_y)
                unit_x, unit_y = dx*1./dist, dy*1./dist
                dx, dy = unit_x*force, unit_y*force
                self.nodes[i].apply_force(-dx, -dy)
