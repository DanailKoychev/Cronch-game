from pygame.sprite import Sprite, Group, Rect
from pygame.math import Vector2 as Vector

class Projectile(Sprite):
    def __init__(self, image, position, speed, aim, damage):
        Sprite.__init__(self)
        self.rect = image.get_rect()
        self.position = position
        self.image = image
        self.speed = speed
        self.aim = aim
        self.damage = damage
        self.movement_vector = self.get_movement_vector()

    @property
    def position(self):
        return self._position
    @position.setter
    def position(self, value):
        self.rect.x = value.x
        self.rect.y = value.y
        self._position = value

    def get_movement_vector(self):
        movement_vector = Vector(self.aim.x - self.position.x,
                                 self.aim.y - self.position.y)
        movement_vector = movement_vector.normalize()
        return movement_vector

    def update(self, time_passed):
        self.position += self.movement_vector * self.speed * time_passed 

    def reflect_horizontally(self, x_position):
        self.aim.x = 2 * x_position - self.aim.x
        self.movement_vector = self.get_movement_vector()

    # def reflect_vertically(self, y_position):
    #




