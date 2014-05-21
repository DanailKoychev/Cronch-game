from pygame.sprite import Sprite, Group, Rect
from copy import copy
from point import *
from projectile import *

MOVING_LEFT = 0
STATIONARY = 1
MOVING_RIGHT = 2
DEAD = 3


class Character():
    def __init__(self, position, size, move_speed, reload_time_millisec,
                 projectile_type, health, damage, aim_speed):
        self.state = STATIONARY
        self.position = position
        self.size = size
        self.move_speed = move_speed
        self.reload_time_millisec = reload_time_millisec
        self.projectile_type = projectile_type
        self.health = health
        self.damage = damage
        self.active_projectiles = []
        self.aim = Point(400, 0)
        self.aim_speed = aim_speed

        self.ready_to_shoot = True
        self.disarmed = False
        self.snared = False
        self.vampire = False

    def move_left(self, time_passed):
        if not self.snared:
            distance_traveled = self.move_speed * time_passed
            self.position.x -= distance_traveled
            self.aim.x -= distance_traveled # alternative aiming system

    def move_right(self, time_passed):
        if not self.snared:
            distance_traveled = self.move_speed * time_passed
            self.position.x += distance_traveled
            self.aim.x += distance_traveled # alternative aiming system
 
    def try_shoot(self, time_passed):
        if self.ready_to_shoot and not self.disarmed:
            self.shoot()
            self.start_reloading()

    def shoot(self):
        shot = Projectile(Point(self.position.x + self.size.y/2,
                                self.position.y),
                          self.projectile_type.size,
                          self.projectile_type.speed,
                          0)
        shot.movement_vector = shot.get_movement_vector(self.aim)
        self.active_projectiles.append(shot)
        return shot

    def start_reloading(self):
        self.ready_to_shoot = False
        self.reload_time_left = self.reload_time_millisec

    def move_aim_left(self, time_passed):
        self.aim.x -= self.aim_speed * time_passed

    def move_aim_right(self, time_passed):
        self.aim.x += self.aim_speed * time_passed

    def update(self, time_passed):
        if self.state == MOVING_LEFT:
            self.move_left(time_passed)
        if self.state == MOVING_RIGHT:
            self.move_right(time_passed)

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
