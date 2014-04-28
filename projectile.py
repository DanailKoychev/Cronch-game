from pygame.sprite import Sprite, Group, Rect
from pygame.math import Vector2 as Vector

class Projectile(Sprite):
    def __init__(self, image, position, speed, aim, effects=[]):
        Sprite.__init__(self)
        self.position = position
        self.image = image
        self.speed = speed
        self.aim = aim
        self.effects = effects
        self.movement_vector = self.get_movement_vector()
        self.rect = image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y

    def get_movement_vector(self):
        movement_vector = Vector(self.aim.x - self.position.x,
                                 self.aim.y - self.position.y)
        movement_vector.normalize()
        return movement_vector

    def move(self, time_passed):
        self.rect.x += self.movement_vector.x * self.speed * time_passed
        self.rect.y += self.movement_vector.y * self.speed * time_passed

    def reflect_vertical(self):
        
