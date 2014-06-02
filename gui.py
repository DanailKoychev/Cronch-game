from game import *

import math
from pygame import sprite 
import pygame, sys
from pygame.locals import *
import random


game = Game(0)


screen = pygame.display.set_mode((Game.FIELD_WIDTH, Game.FIELD_HEGHT))

background = pygame.image.load("assets/background.png").convert()


# ---- choose image depending on player type
player_one_image = pygame.image.load("assets/character.png").convert()
player_one_image = pygame.transform.scale(player_one_image, \
                   (game.player_1.size.x, game.player_1.size.y))

player_two_image = pygame.image.load("assets/character.png").convert()
player_two_image = pygame.transform.scale(player_two_image, \
                   (game.player_1.size.x, game.player_1.size.y))
player_two_image = pygame.transform.flip(player_two_image, False, True)

dead_player_image = pygame.image.load("assets/dead_character.png").convert()
dead_player_image = pygame.transform.scale(dead_player_image, \
                    (game.player_1.size.x, game.player_1.size.y))

projectile_image = pygame.image.load("assets/projectile.jpg").convert()
projectile_image = pygame.transform.scale(projectile_image, \
 (game.player_1.projectile_type.size.x, game.player_1.projectile_type.size.y))

wall_image = pygame.image.load("assets/wall.jpg").convert()
wall_image = pygame.transform.scale(wall_image, (100, 5))

#aim_image = pygame.image.load("assets/wall.jpg").convert()
#aim_image = pygame.transform.scale(wall_image, (5, 5))

#font = pygame.font.SysFont("monospace", 30)

def render_via_pygame(game):
    screen.blit(background, (0, 0))

    players = (game.player_1, game.player_2)
    images = [player_one_image, player_two_image]

    for player, image in zip(players, images):
        for projectile in player.active_projectiles:
            screen.blit(projectile_image, \
                        (projectile.position.x - projectile.size.x / 2, \
                         projectile.position.y - projectile.size.y / 2))

        if not player.alive:
            image = dead_player_image
        screen.blit(pygame.transform.rotate(image, get_leaning(player)), \
                    (player.position.x - player.size.x / 2, \
                     player.position.y - player.size.y / 2))

    for wall in game.walls:
        screen.blit(wall_image, (wall.position.x - wall.size.x/2, \
                                 wall.position.y - wall.size.y/2))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

def get_leaning(player):
    if player.position.x == player.aim.x:
        return 0
    else:
        return math.atan((player.aim.x - player.position.x) / \
                         (player.aim.y - player.position.y)) * 57.3 
                         # 57.3 - approximate degree to radian ratio
