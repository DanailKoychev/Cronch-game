import pygame
from pygame.sprite import Sprite
import random

from point import *

WALL_IMAGE = pygame.image.load("assets/wall.jpg")
WALL_SPEED = 0.1
POWER_UPS = {0:'VAMPIRE', 1:'SPEED_UP', 2:'BONUS_HP', 3:'DISARM', 4:'SNARE', 5:'DAMAGE', 6:'CLEANSE'} # , 7:'INVISIBILITY'}
VAMPIRE_PERCENT = 30
SPEED_UP_PERCENT = 20
BONUS_HP_VALUE = 50
DISARM_TIME_MILLISEC = 4000
SNARE_TIME_MILLISEC = 2000
DAMAGE_UP_PERCENT = 30

# REFLECT_DAMAGE
# 'OLAF' SPEED PER HP MISSING
# TF 2-CARD


class Wall(Sprite):
    def __init__(self, from_left, field_width, field_height):
        Sprite.__init__(self)
        self.from_left = from_left
        self.image = WALL_IMAGE
        self.rect = self.image.get_rect()
        self.speed = WALL_SPEED
        self._position = Point(0,0)
        self._position.y = field_height/2 - WALL_IMAGE.get_height() / 2
        if from_left:
            self._position.x = 0 - WALL_IMAGE.get_width()
        else:
            self._position.x = field_width
        self.position = self._position
        self.power_up = None

    @property
    def position(self):
        return self._position
    @position.setter
    def position(self, value):
        self.rect.x = value.x
        self.rect.y = value.y
        self._position = value

    def move_left(self, time_passed):
        self._position.x -= self.speed * time_passed
        self.position = self.position

    def move_right(self, time_passed):
        self._position.x += self.speed * time_passed
        self.position = self.position

    def get_power_up(self, power_up=None):
        if power_up is not None:
            self.power_up = power_up
        else:
            power_up = POWER_UPS[random.randint(0, len(POWER_UPS))]



    def give_speed_up(self, character):
        character.speed *= 1 + SPEED_UP_PERCENT / 100

    def give_bonus_hp(self, character):
        character.health += BONUS_HP_VALUE

    def give_vampire(self, character):
        character.vampire = VAMPIRE_PERCENT / 100

    def give_disarm(self, character):
        character.disarmed = True
        character.disarmed_time = DISARM_TIME_MILLISEC

    def give_snare(self, character):
        character.snared = True
        character.snare_time_left = SNARE_TIME_MILLISEC

    def give_gamage(self, character):
        character.damage *= 1 + DAMAGE_UP_PERCENT / 100



