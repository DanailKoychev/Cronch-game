import random

from point import *

class Wall():
    HEAL = 0
    SNARE = 1
    VAMIPIRE = 2
    SPEED_UP = 3
    DISARM = 4
    
    VAMPIRE_PERCENT = 60
    VAMPIRE_TIME = 10000
    SPEED_UP_PERCENT = 20
    HEAL_VALUE = 30
    DISARM_TIME_MILLISEC = 4000
    SNARE_TIME_MILLISEC = 2000
    DAMAGE_UP_PERCENT = 30

    SPEED = 0.09

    def __init__(self, size, going_right, field_width, field_height):
        self.size = size
        self.going_right = going_right
        self.speed = Wall.SPEED
        self.position = Point(0,0)
        self.position.y = field_height/2
        if going_right:
            self.position.x = 0 - self.size.x / 2
        else:
            self.position.x = field_width + self.size.x / 2
        #self.position = self.position
        self.power_up = None

    def move_left(self, time_passed):
        self.position.x -= self.speed * time_passed

    def move_right(self, time_passed):
        self.position.x += self.speed * time_passed

    def update(self, time_passed):
        if self.going_right:
            self.move_right(time_passed)
        else:
            self.move_left(time_passed)

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
    
    
