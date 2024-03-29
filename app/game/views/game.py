# import sys
# sys.path.append('/Users/ak/PycharmProjects/MakerBreakerGame')

import arcade

from app.game.components.hypergraph import HyperGraph
from app.game.config.constants import Constants
from app.game.engine.data import test_hypergraph
from app.game.engine.interface import SelectableObject, PhysicsObject
from app.game.views.game_over import GameOverView


class GameView(arcade.View):
    def __init__(self, main_menu_view, pre_adjust=False):
        # super().__init__(Constants.WIDTH, Constants.HEIGHT, title="Maker Breaker Game")
        super().__init__()

        self.main_menu_view = main_menu_view

        self.is_makers_turn = True
        self.makers_nodes = []
        self.breakers_nodes = []

        self.hypergraph = HyperGraph(Constants.WIDTH, Constants.HEIGHT, Constants.NODE_RADIUS, Constants.FONT_SIZE)
        self.right_mouse_bound_object: PhysicsObject | SelectableObject | None = None
        self.hover_bound_object: PhysicsObject | SelectableObject | None = None

        self.pre_adjust = pre_adjust
        self.setup()

    def setup(self):
        arcade.set_background_color(Constants.BACKGROUND_COLOR)
        self.hypergraph.create_graph(nodes=test_hypergraph['nodes'], edges=test_hypergraph['edges'])
        if self.pre_adjust:
            self.hypergraph.pre_self_adjust()

    def on_draw(self):
        arcade.start_render()

        self.hypergraph.draw_graph()
        self.hypergraph.self_adjust()
        self.hypergraph.self_center()

        self._draw_next_players_turn_text()

        self._draw_color_palette()
        self._draw_right_mouse_bound_obj()

    def on_mouse_motion(self, x, y, dx, dy):
        """Called when the mouse moves."""
        # handle mouse bound object
        self._handle_rmb_object(x, y)

        # handle on-hover
        self._handle_on_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        """Called when the mouse is pressed"""
        # left mouse button. pick a color.
        if button == 1:
            self._handle_set_color(x, y)

        # right mouse button. move an object.
        if button == 4:
            self._handle_set_rmb(x, y)

    # def on_mouse_release(self, x, y, button, modifiers):
    #     """Called when the mouse is released"""
    #     if button == 1:
    #         self.mouse_bound_object = None

    def _handle_rmb_object(self, x, y):
        if self.right_mouse_bound_object is not None:
            self._set_velocity_to_right_mouse_bound_object(x, y)

    def _handle_on_hover(self, x, y):
        if self.right_mouse_bound_object is not None:
            self.hover_bound_object = self.right_mouse_bound_object
        elif self.hover_bound_object is None or not self.hypergraph.is_point_on_color_palette(x, y):
            node = self.hypergraph.find_closest_node(x, y)
            if self.hover_bound_object is not None and node != self.hover_bound_object:
                self._clear_node_color()

            if node is not None and node != self.hover_bound_object:
                self._set_node_color(node)

    def _handle_set_color(self, x, y):
        if self.right_mouse_bound_object is None:
            if self.hover_bound_object is not None:
                color = self.hypergraph.get_palette_color(x, y)
                if color is not None:
                    self.hover_bound_object.set_perm_color(color)
                    if self.is_makers_turn:
                        self.makers_nodes.append(self.hover_bound_object)
                    else:
                        self.breakers_nodes.append(self.hover_bound_object)
                    self.is_makers_turn = not self.is_makers_turn

                    if self._has_destructor_won():
                        self._game_over("Destructor has won the game!")
                    if self._has_constructor_won():
                        self._game_over("Constructor has won the game!")

    def _handle_set_rmb(self, x, y):
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

    def _draw_next_players_turn_text(self):
        if self.is_makers_turn:
            text = "Maker's turn"
        else:
            text = "Breaker's turn"
        arcade.draw_text(text, 50, self.window.height - 50,
                         arcade.color.HONEYDEW, font_size=16)

    def _game_over(self, text):
        game_over_view = GameOverView(self.main_menu_view, text)
        self.window.show_view(game_over_view)

    def _has_destructor_won(self):
        for node in self.hypergraph.nodes:
            if not node.has_color_set() and not len(self.hypergraph.get_available_colors(node)):
                return True
        return False

    def _has_constructor_won(self):
        for node in self.hypergraph.nodes:
            if not node.has_color_set():
                return False
        return True

    def _draw_right_mouse_bound_obj(self):
        if self._can_draw_right_mouse_bound_obj():
            self.right_mouse_bound_object.update()

    def _draw_color_palette(self):
        if self._can_draw_color_palette():
            available_colors = self.hypergraph.get_available_colors(self.hover_bound_object)
            if len(available_colors):
                self.hypergraph.set_palette_colors(available_colors)
                self.hypergraph.draw_color_palette()
                self.hypergraph.update_color_palette(self.hover_bound_object.point_x,
                                                     self.hover_bound_object.point_y)

    def _can_draw_right_mouse_bound_obj(self):
        return self.right_mouse_bound_object is not None

    def _can_draw_color_palette(self):
        if self.right_mouse_bound_object is None:
            if self.hover_bound_object is not None:
                if not self.hover_bound_object.has_color_set():
                    return True
        return False

    def _set_velocity_to_right_mouse_bound_object(self, vel_x, vel_y):
        self.right_mouse_bound_object.vel_x = vel_x
        self.right_mouse_bound_object.vel_y = vel_y

    def _set_position_to_color_palette(self, x, y):
        self.hypergraph.color_palette.point_x = x
        self.hypergraph.color_palette.point_y = y

    def _clear_node_color(self):
        # self.hover_bound_object.color = self.hover_bound_object.default_color
        for edge in self.hypergraph.get_edges(self.hover_bound_object):
            edge.color = edge.default_color
        self.hover_bound_object = None

    def _set_node_color(self, node):
        self.hover_bound_object = node
        # self.hover_bound_object.color = arcade.csscolor.ROYAL_BLUE
        for edge in self.hypergraph.get_edges(self.hover_bound_object):
            edge.color = arcade.csscolor.VIOLET
        self._set_position_to_color_palette(node.point_x, node.point_y)
