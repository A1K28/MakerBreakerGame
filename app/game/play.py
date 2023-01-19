import arcade

from app.game.config.constants import Constants
from app.game.views.main_menu import MainMenuView

if __name__ == '__main__':
    window = arcade.Window(Constants.WIDTH, Constants.HEIGHT, title="Maker Breaker Game")
    start_view = MainMenuView()
    window.show_view(start_view)
    arcade.run()
