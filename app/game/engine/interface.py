import arcade


class MovableObject:
    color: arcade.csscolor = None
    default_color: arcade.csscolor = None

    def update(self, x: float, y: float):
        """Move an object to its new position"""
        pass

    def select(self):
        """Selects an object"""
        pass

    def deselect(self):
        """Deselects an object"""
        pass
