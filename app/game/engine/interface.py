import arcade

from app.game.engine.types import Point2D


class SelectableObject:
    is_selected: bool = False
    color: arcade.csscolor = None
    default_color: arcade.csscolor = None

    def select(self):
        """Selects an object"""
        self.is_selected = True

    def deselect(self):
        """Deselects an object"""
        self.is_selected = False

    def has_color_set(self):
        return self.color != self.default_color

    def set_perm_color(self, color):
        if not self.has_color_set():
            self.color = color


class PhysicsObject:
    point_x: float = None
    point_y: float = None

    vel_x: float = None
    vel_y: float = None

    def update(self):
        """Move an object to its new position"""
        pass

    def apply_force(self, f_x: float, f_y: float):
        """Apply the given force to an object"""
        pass

    def to_point(self) -> Point2D:
        """Transform the object into a Point2D object"""
        return Point2D(self.point_x, self.point_y)
