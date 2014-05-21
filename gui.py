from game import *

from pygame import sprite 
import pygame, sys
from pygame.locals import *
import random


game = Game(0)


screen = pygame.display.set_mode((Game.FIELD_WIDTH, Game.FIELD_HEGHT))

# ---- choose image depending on player type
player_one_image = pygame.image.load("assets/character.jpg").convert()
player_one_image = pygame.transform.scale(player_one_image, (game.player_1.size.x, game.player_1.size.y))

player_two_image = pygame.image.load("assets/character.jpg").convert()
player_two_image = pygame.transform.scale(player_two_image, (game.player_1.size.x, game.player_1.size.y))

pl_one_projectile_image = pygame.image.load("assets/projectile.jpg").convert()
pl_one_projectile_image = pygame.transform.scale(pl_one_projectile_image, (game.player_1.projectile_type.size[0], game.player_1.projectile_type.size[1]))

pl_two_projectile_image = pygame.image.load("assets/projectile.jpg").convert()
pl_two_projectile_image = pygame.transform.scale(pl_two_projectile_image, (game.player_1.size.x, game.player_1.size.y))

wall_iamge = pygame.image.load("assets/wall.jpg").convert()
wall_iamge = pygame.transform.scale(wall_iamge, (game.player_1.size.x, game.player_1.size.y))



def render_via_pygame(game):
    screen.fill((10,20,40))
    players = [game.player_1, game.player_2]

    for player in players:
        for projectile in player.active_projectiles:
            screen.blit(pl_one_projectile_image, (projectile.position.x, projectile.position.y))
        screen.blit(player_one_image, (player.position.x, player.position.y))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
