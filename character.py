from pygame.sprite import Sprite, Group, Rect
from copy import copy

class Character(Spire):
    def __init__(self, image, position, move_speed, time_between_shots,
                 projectile_type, health, damage):
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
        self.aim = (0, 0)

    def move_left(self, time_passed):
        distance_traveled = self.speed * time_passed
        self.position.x -= distance_traveled
        self.aim.x -= distance_traveled

    def move_righ(self, time_passed):
        distance_traveled = self.speed * time_passed
        self.position.x += distance_traveled
        self.aim.x += distance_traveled

    # def shoot(self, projectile=None):
    def shoot(self): 
        projectile = copy(projectile_type)    
        self.active_projectiles.append(projectile)
        projectile.position = self.position
        projectile.aim = self.aim
