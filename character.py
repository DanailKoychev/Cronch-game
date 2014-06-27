
from point import *
from projectile import *
from controls import *

AIM_SPEED = 0.7

class Character():
    def __init__(self, position, size, speed, reload_time_millisec,
                 projectile_type, health, damage):
        self.state = None
        self.position = position
        self.size = size
        self.speed = speed
        self.reload_time_millisec = reload_time_millisec
        self.projectile_type = projectile_type
        self.health = health
        self.damage = damage
        self.own_projectiles = []
        self.aim = Point(0, 0)
        self.aim_speed = AIM_SPEED

        self.ready_to_shoot = True
        self.disarmed = False
        self.snared = False
        self.alive = True
        self.vampire = False

    def move_left(self, time_passed):
        if not self.snared:
            distance_traveled = self.speed * time_passed
            self.position.x -= distance_traveled
            self.aim.x -= distance_traveled

    def move_right(self, time_passed):
        if not self.snared:
            distance_traveled = self.speed * time_passed
            self.position.x += distance_traveled
            self.aim.x += distance_traveled
 
    def try_shoot(self):
        if self.ready_to_shoot and not self.disarmed:
            self.start_reloading()
            return self.shoot()

    def shoot(self):
        shot = Projectile(Point(self.position.x,self.position.y),
                          Point(self.projectile_type.size.x,
                                self.projectile_type.size.y),
                          self.projectile_type.speed,
                          self.damage,
                          self.aim,
                          self)
        shot.movement_vector = shot.get_movement_vector(self.aim)
        self.own_projectiles.append(shot)
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

        if self.vampire:
            self.vampire_time_left -= time_passed
            if self.vampire_time_left <= 0:
                self.vampire = False

        if self.health <= 0:
            self.alive = False

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
    