import arcade

from app.game.engine.types import Point2D


class MovableObject:
    def update(self, x: float, y: float):
        """Move an object to its new position"""
        pass


class SelectableObject:
    color: arcade.csscolor = None
    default_color: arcade.csscolor = None

    def select(self):
        """Selects an object"""
        pass

    def deselect(self):
        """Deselects an object"""
        pass


class PhysicsObject:
    point_x: float = None
    point_y: float = None

    def to_point(self) -> Point2D:
        """Transform the object into a Point2D object"""
        pass

    def apply_force(self, dx: float, dy: float):
        """Apply the given force to an object"""
        pass
