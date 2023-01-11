import math
import arcade
from app.service.hypergraph import decompose_edges_by_len, test_hypergraph


def draw_graph(nodes, edges):
    mid_x = 1280/2
    mid_y = 720/2
    radii = 2*len(nodes) + 100
    fi = 0
    step = 360 * 1. / len(nodes)
    for i, node in enumerate(nodes):
        x = math.cos(math.radians(fi)) * radii
        y = math.sin(math.radians(fi)) * radii
        draw_node(mid_x+x, mid_y+y, str(i+1))
        fi = (fi+step) % 360


def draw_node(x, y, tag, radius=12, font_size=10):
    if len(tag) > 2:
        raise ValueError(f"Tag ({tag}) length is greater than 2")
    text_x = x-radius/2+2
    text_y = y-radius/2+2
    if len(tag) == 2:
        font_size -= 2
        text_x -= 2
    arcade.draw_circle_filled(x, y, radius, arcade.csscolor.ORANGE)
    arcade.draw_text(tag, text_x, text_y, font_size=font_size, color=arcade.csscolor.BLACK)


class MakerBreakerGame:
    DARK_BLUE_COLOR = (0, 48, 73)

    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height

    def run(self):
        arcade.open_window(self.width, self.height, "Drawing Example")

        arcade.set_background_color(self.DARK_BLUE_COLOR)

        arcade.start_render()

        draw_graph(nodes=test_hypergraph['nodes'], edges=decompose_edges_by_len(test_hypergraph['edges']))

        arcade.finish_render()

        arcade.run()


if __name__ == '__main__':
    game = MakerBreakerGame()
    game.run()
