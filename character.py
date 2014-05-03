from pygame.sprite import Sprite, Group, Rect
from copy import copy
from point import *
from projectile import *

class Character(Sprite):
    def __init__(self, image, position, move_speed, time_between_shots,
                 projectile_type, health, damage, aim_speed):
        Sprite.__init__(self)
        self.position = position
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y
        self.move_speed = move_speed
        self.time_between_shots = time_between_shots
        self.projectile_type = projectile_type
        self.health = health
        self.damage = damage
        self.active_projectiles = []
        self.aim = Point(100, 0)
        self.aim_speed = aim_speed

    def move_left(self, time_passed):
        distance_traveled = self.move_speed * time_passed
        self.position.x -= distance_traveled
        self.rect.x = self.position.x
        self.aim.x -= distance_traveled

    def move_righ(self, time_passed):
        distance_traveled = self.move_speed * time_passed
        self.position.x += distance_traveled
        self.rect.x = self.position.x
        self.aim.x += distance_traveled
 
    def shoot(self):
        shot = Projectile(self.projectile_type.image,
                          Point(self.position.x, self.position.y),
                          self.projectile_type.speed,
                          Point(self.aim.x, self.aim.y),
                          0)
        shot.movement_vector = shot.get_movement_vector()
        self.active_projectiles.append(shot)
        return shot

    def move_aim_left(self, time_passed):
        self.aim.x -= self.aim_speed * time_passed

    def move_aim_right(self, time_passed):
        self.aim.x += self.aim_speed * time_passed
