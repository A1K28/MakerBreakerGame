import arcade


class MakerBreakerGame:
    DARK_BLUE_COLOR = (0, 48, 73)

    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height

    def run(self):
        arcade.open_window(self.width, self.height, "Drawing Example")

        arcade.set_background_color(self.DARK_BLUE_COLOR)
        # arcade.set_background_color(arcade.csscolor.BISQUE)

        arcade.start_render()

        arcade.draw_circle_filled(100, 100, 10, arcade.csscolor.ORANGE)

        arcade.finish_render()

        arcade.run()


if __name__ == '__main__':
    game = MakerBreakerGame()
    game.run()
