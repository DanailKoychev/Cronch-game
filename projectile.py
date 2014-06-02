from pygame.math import Vector2 as Vector

import point

class Projectile():
    def __init__(self, position, size, speed, damage, aim, master=None):
        self.position = position
        self.size = size
        self.speed = speed
        self.damage = damage
        self.aim = point.Point(aim.x, aim.y)
        self.master = master

    def get_movement_vector(self, aim):
        movement_vector = Vector(aim.x - self.position.x,
                                 aim.y - self.position.y)
        movement_vector = movement_vector.normalize()
        return movement_vector

    def update(self, time_passed):
        self.position += self.movement_vector * self.speed * time_passed

    def reflect_horizontally(self, x_position):
        self.position.x = x_position
        self.aim.x = 2 * x_position - self.aim.x
        self.movement_vector.x = -self.movement_vector.x

    @property
    def x(self):
        return self.position.x
    @x.setter
    def x(self, value):
        self.position = value

    @property
    def y(self):
        return self.position.y
    @y.setter
    def y(self, value):
        self.position.y = value
    
    
