from pygame.locals import *
import pygame

class Controls:
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    USE_SKILL = 3
    AIM_LEFT = 4
    AIM_RIGHT = 5
    SHOOT = 6

    def get_keyboard_input_player_2():
        instructions = []
        keys = pygame.key.get_pressed()
        if keys[K_KP1]:
            instructions.append(Controls.MOVE_LEFT)
        if keys[K_KP3]:
            instructions.append(Controls.MOVE_RIGHT)
        if keys[K_KP5]:
            instructions.append(Controls.USE_SKILL)
        if keys[K_LEFT]:
            instructions.append(Controls.AIM_LEFT)
        if keys[K_RIGHT]:
            instructions.append(Controls.AIM_RIGHT)
        if keys[K_UP]:
            instructions.append(Controls.SHOOT)
        return instructions

    def get_keyboard_input_player_1():
        instructions = []
        keys = pygame.key.get_pressed()
        if keys[K_j]:
            instructions.append(Controls.MOVE_LEFT)
        if keys[K_g]:
            instructions.append(Controls.MOVE_RIGHT)
        if keys[K_y]:
            instructions.append(Controls.USE_SKILL)
        if keys[K_a]:
            instructions.append(Controls.AIM_LEFT)
        if keys[K_d]:
            instructions.append(Controls.AIM_RIGHT)
        if keys[K_w]:
            instructions.append(Controls.SHOOT)
        return instructions 