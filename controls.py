from pygame import key
from character import *
import pygame

from character import *
from projectile import *
from pygame.math import Vector2 as Vector
from point import *
from wall import *

from pygame import sprite 
import pygame, sys
from pygame.locals import *
import random

MOVE_LEFT = 1
MOVE_RIGHT = 2
USE_SKILL = 3
AIM_LEFT = 4
AIM_RIGHT = 5
SHOOT = 6

def get_keyboard_input():
    instructions = []
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        instructions.append(MOVE_LEFT)
    if keys[K_RIGHT]:
        instructions.append(MOVE_RIGHT)
    if keys[K_DOWN]:
        instructions.append(USE_SKILL)
    if keys[K_a]:
        instructions.append(AIM_LEFT)
    if keys[K_d]:
        instructions.append(AIM_RIGHT)
    if keys[K_w]:
        instructions.append(SHOOT)
    return instructions
