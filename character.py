from pygame.sprite import Sprite, Group, Rect
from copy import copy
from point import *
from projectile import *

class Character(Sprite):
    def __init__(self, image, position, move_speed, reload_time_millisec,
                 projectile_type, health, damage, aim_speed):
        Sprite.__init__(self)
        self.rect = image.get_rect()
        self.position = position
        self.image = image
        self.move_speed = move_speed
        self.reload_time_millisec = reload_time_millisec
        self.projectile_type = projectile_type
        self.health = health
        self.damage = damage
        self.active_projectiles = Group()
        self.aim = Point(400, 0)
        self.aim_speed = aim_speed

        self.ready_to_shoot = True
        self.disarmed = False
        self.snared = False
        self.vampire = False

    @property
    def position(self):
        return self._position
    @position.setter
    def position(self, value):
        self.rect.x = value.x
        self.rect.y = value.y
        self._position = value

    def move_left(self, time_passed):
        if not self.snared:
            distance_traveled = self.move_speed * time_passed
            self.position.x -= distance_traveled
            self.rect.x = self.position.x
            self.aim.x -= distance_traveled # alternative aiming system

    def move_righ(self, time_passed):
        if not self.snared:
            distance_traveled = self.move_speed * time_passed
            self.position.x += distance_traveled
            self.rect.x = self.position.x
            self.aim.x += distance_traveled # alternative aiming system
 
    def try_shoot(self, time_passed):
        if self.ready_to_shoot and not self.disarmed:
            self.shoot()
            self.start_reloading()

    def shoot(self):
        shot = Projectile(self.projectile_type.image,
                          Point(self.position.x + self.rect.width/2,
                                self.position.y),
                          self.projectile_type.speed,
                          #self.aim,
                          0)
        shot.movement_vector = shot.get_movement_vector(self.aim)
        self.active_projectiles.add(shot)
        return shot

    def start_reloading(self):
        self.ready_to_shoot = False
        self.reload_time_left = self.reload_time_millisec

    def move_aim_left(self, time_passed):
        self.aim.x -= self.aim_speed * time_passed

    def move_aim_right(self, time_passed):
        self.aim.x += self.aim_speed * time_passed

    def update(self, time_passed):
        if self.disarmed:
            self.disarm_time_left -= time_passed
            if self.disarm_time_left <= 0:
                self.disarmed = False
        if self.snared:
            self.snare_time_left -= time_passed
            if self.snare_time_left <=0:
                self.snared = False
        if not self.ready_to_shoot:
            self.reload_time_left -= time_passed
            if self.reload_time_left <= 0:
                self.ready_to_shoot = True
