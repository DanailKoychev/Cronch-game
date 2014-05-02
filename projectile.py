from pygame.sprite import Sprite, Group, Rect
from pygame.math import Vector2 as Vector

class Projectile(Sprite):
    def __init__(self, image, position, speed, aim, effects=[]):
        Sprite.__init__(self)
        self.position = position
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y
        self.speed = speed
        self.aim = aim
        self.effects = effects
        self.movement_vector = self.get_movement_vector()

    def get_movement_vector(self):
        movement_vector = Vector(self.aim.x - self.rect.x,
                                 self.aim.y - self.rect.y)
        movement_vector = movement_vector.normalize()
        return movement_vector

    def update(self, time_passed):
        self.position.x += self.movement_vector.x * self.speed * time_passed
        self.position.y += self.movement_vector.y * self.speed * time_passed
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def reflect_horizontally(self, x_position):
        self.aim.x = 2 * x_position - self.aim.x
        self.movement_vector = self.get_movement_vector()

    # TODO: position aim on the other side of the screen
    # def reflect_vertically(self, y_position):
    #     self.aim.y = 405
    #     self.movement_vector = self.get_movement_vector()




