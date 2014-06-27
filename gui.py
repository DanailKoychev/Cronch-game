import math
import pygame, sys
from pygame.locals import *
import random

from game import *

# --------------------------------------------!
game = Game(0)
# --------------------------------------------!

screen = pygame.display.set_mode((game.field_width, game.field_height))

background = pygame.image.load("assets/background.png").convert()

player_one_image = pygame.image.load("assets/character.png").convert()
player_one_image = pygame.transform.scale(player_one_image, \
                   (game.player_1.size.x, game.player_1.size.y))

player_two_image = pygame.image.load("assets/character.png").convert()
player_two_image = pygame.transform.scale(player_two_image, \
                   (game.player_2.size.x, game.player_2.size.y))
player_two_image = pygame.transform.flip(player_two_image, False, True)

dead_player_image = pygame.image.load("assets/dead_character.png").convert()
dead_player_image = pygame.transform.scale(dead_player_image, \
                    (game.player_1.size.x, game.player_1.size.y))

projectile_image = pygame.image.load("assets/projectile.jpg").convert()
projectile_image = pygame.transform.scale(projectile_image, \
 (game.player_1.projectile_type.size.x, game.player_1.projectile_type.size.y))

projectile_vampire = pygame.image.load("assets/projectile_vampire.png").convert()
projectile_vampire = pygame.transform.scale(projectile_vampire, \
 (game.player_1.projectile_type.size.x, game.player_1.projectile_type.size.y))

wall_image = pygame.image.load("assets/wall.jpg").convert()
wall_image = pygame.transform.scale(wall_image, (100, 5))

wall_heal = pygame.image.load("assets/wall_heal.jpg").convert()
wall_heal = pygame.transform.scale(wall_heal, (100, 8))

wall_speed_up = pygame.image.load("assets/wall_speed_up.jpg").convert()
wall_speed_up = pygame.transform.scale(wall_speed_up, (100, 8))

wall_snare = pygame.image.load("assets/wall_snare.jpg").convert()
wall_snare = pygame.transform.scale(wall_snare, (100, 8))

wall_disarm = pygame.image.load("assets/wall_disarm.jpg").convert()
wall_disarm = pygame.transform.scale(wall_disarm, (100, 8))

wall_vampire = pygame.image.load("assets/wall_vampire.jpg").convert()
wall_vampire = pygame.transform.scale(wall_vampire, (100, 8))

pygame.font.init()
myfont = pygame.font.SysFont("monospace", 15)

#aim_image = pygame.image.load("assets/wall.jpg").convert()
#aim_image = pygame.transform.scale(wall_image, (5, 5))

#font = pygame.font.SysFont("monospace", 30)

def render_via_pygame(game):
    screen.blit(background, (0, 0))

    players = (game.player_1, game.player_2)
    images = [player_one_image, player_two_image]

    for projectile in game.active_projectiles:
        if projectile.owner.vampire == True:
            image = projectile_vampire
        else:
            image = projectile_image
        image = pygame.transform.scale(image, (int(projectile.size.x),
                                               int(projectile.size.y)))
        screen.blit(image, \
                    (projectile.position.x - projectile.size.x / 2, \
                    projectile.position.y - projectile.size.y / 2))

    for player, image in zip(players, images):
        if not player.alive:
            image = dead_player_image
        screen.blit(pygame.transform.rotate(image, get_leaning(player)), \
                    (player.position.x - player.size.x / 2, \
                     player.position.y - player.size.y / 2))

    hp_1 = myfont.render(str(int(game.player_1.health)), 1, (255,255,0))
    screen.blit(hp_1, (game.player_1.x, game.player_1.y + game.player_1.size.y - 25))
    hp_2 = myfont.render(str(int(game.player_2.health)), 1, (255,255,0))
    screen.blit(hp_2, (game.player_2.x, game.player_2.y - game.player_2.size.y + 15))

    for wall in game.walls:
        if wall.power_up == HEAL:
            screen.blit(wall_heal, (wall.position.x - wall.size.x/2, \
                        wall.position.y - wall.size.y/2))        
        elif wall.power_up == SPEED_UP:
            screen.blit(wall_speed_up, (wall.position.x - wall.size.x/2, \
                        wall.position.y - wall.size.y/2)) 
        elif wall.power_up == SNARE:
            screen.blit(wall_snare, (wall.position.x - wall.size.x/2, \
                        wall.position.y - wall.size.y/2)) 
        elif wall.power_up == DISARM:
            screen.blit(wall_disarm, (wall.position.x - wall.size.x/2, \
                        wall.position.y - wall.size.y/2)) 
        elif wall.power_up == VAMIPIRE:
            screen.blit(wall_vampire, (wall.position.x - wall.size.x/2, \
                        wall.position.y - wall.size.y/2))
        else:
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
                         # 57.3 - approximate degree-to-radian ratio
