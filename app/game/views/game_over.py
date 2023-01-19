import arcade

from app.game.config.constants import Constants


class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self, main_menu_view: arcade.View, text: str):
        """ This is run once when we switch to this view """
        super().__init__()
        self.text = text
        self.main_menu_view = main_menu_view

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(Constants.DARK_BLUE_COLOR)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text(self.text, self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to try again", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        self.main_menu_view.show_game()
        # self.window.show_view(self.main_menu_view)
