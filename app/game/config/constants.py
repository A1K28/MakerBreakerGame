import arcade.csscolor


class Constants:
    # WIDTH, HEIGHT = arcade.window_commands.get_display_size()
    WIDTH = 1280
    HEIGHT = 720
    NODE_RADIUS = 10
    EDGE_WIDTH = 1.2
    BACKGROUND_COLOR = (0, 48, 73)
    NODE_INNER_COLOR = arcade.csscolor.WHITE
    NODE_OUTER_COLOR = BACKGROUND_COLOR
    EDGE_COLOR = arcade.csscolor.WHITE
    FONT_SIZE = 10
    INFINITY = float('inf')
    COULOMB_K = 8.988 * (10 ** 5)
    COULOMB_Q = 0.5
    HOOKE_K = 0.001
    COLOR_PALETTE_LIST = [arcade.csscolor.CYAN, arcade.csscolor.MEDIUM_VIOLET_RED, arcade.csscolor.LIME]
    DRAG_CONSTANT = 0.1
