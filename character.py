
from point import *
from projectile import *
from controls import *

MOVING_LEFT = 0
STATIONARY = 1
MOVING_RIGHT = 2
DEAD = 3

class Character():
    def __init__(self, position, size, speed, reload_time_millisec,
                 projectile_type, health, damage, aim_speed):
        self.state = STATIONARY
        self.position = position
        self.size = size
        self.speed = speed
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
        self.alive = True

    def __move_left(self, time_passed):
        if not self.snared:
            distance_traveled = self.speed * time_passed
            self.position.x -= distance_traveled
            self.aim.x -= distance_traveled # alternative aiming system

    def __move_right(self, time_passed):
        if not self.snared:
            distance_traveled = self.speed * time_passed
            self.position.x += distance_traveled
            self.aim.x += distance_traveled # alternative aiming system
 
    def try_shoot(self):
        if self.ready_to_shoot and not self.disarmed:
            self.shoot()
            self.start_reloading()

    def shoot(self):
        shot = Projectile(Point(self.position.x,
                                self.position.y),
                          self.projectile_type.size,
                          self.projectile_type.speed,
                          self.projectile_type.damage,
                          self.aim)
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
            self.__move_left(time_passed)
        if self.state == MOVING_RIGHT:
            self.__move_right(time_passed)

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

        if self.health <= 0:
            self.alive = False

    def use_input(self, instruction_set, time_passed):
            if MOVE_LEFT in instruction_set:
                self.state = MOVING_LEFT
            elif MOVE_RIGHT in instruction_set:
                self.state = MOVING_RIGHT
            else:
                self.state = STATIONARY 
            if USE_SKILL in instruction_set:
                raise NotImplementedError("no skills yet")
            if AIM_LEFT in instruction_set:
                self.move_aim_left(time_passed)
            if AIM_RIGHT in instruction_set:
                self.move_aim_right(time_passed)
            if SHOOT in instruction_set:
                self.try_shoot()


    def get_hit(self, projectile):
        self.health -= projectile.damage

    @property
    def x(self):
        return self.position.x
    @x.setter
    def x(self, value):
        self.position.x = value
    
    @property
    def y(self):
        return self.position.y
    @y.setter
    def y(self, value):
        self.position.y = value
    