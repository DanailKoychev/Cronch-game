import math
import pygame, sys
from pygame.locals import *
import random
import time

import controls
import tank
import berserker
import tank_bot
import berserker_bot
from wall import Wall

from game import *

FPS = 120
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((Game.FIELD_WIDTH, Game.FIELD_HEIGHT))
game = Game("berserker", "tank")

background = pygame.image.load("assets/background.png").convert()

myfont = pygame.font.SysFont("monospace", 15)

player_1_image = pygame.image.load("assets/berserker.png").convert()
player_1_image = pygame.transform.scale(player_1_image, \
                   (game.player_1.size.x, game.player_1.size.y))
player_2_image = pygame.image.load("assets/tank.png").convert()
player_2_image = pygame.transform.scale(player_2_image, \
                   (game.player_2.size.x, game.player_2.size.y))
player_2_image = pygame.transform.flip(player_2_image, False, True)

dead_player_image = pygame.image.load("assets/dead_character.png").convert()
dead_player_image = pygame.transform.scale(dead_player_image, \
                    (game.player_1.size.x, game.player_1.size.y))

projectile_image = pygame.image.load("assets/projectile.png").convert()
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


def draw_projectiles(game):
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


def draw_health(game):
    hp_1 = myfont.render(str(int(game.player_1.health)), 1, (255,255,0))
    screen.blit(hp_1, (game.player_1.x, game.player_1.y + game.player_1.size.y / 2 + 10))
    hp_2 = myfont.render(str(int(game.player_2.health)), 1, (255,255,0))
    screen.blit(hp_2, (game.player_2.x, game.player_2.y - game.player_2.size.y / 2 - 20))    


def draw_walls(game):
    for wall in game.walls:
        if wall.power_up == Wall.HEAL:
            screen.blit(wall_heal, (wall.position.x - wall.size.x/2, \
                        wall.position.y - wall.size.y/2))        
        elif wall.power_up == Wall.SPEED_UP:
            screen.blit(wall_speed_up, (wall.position.x - wall.size.x/2, \
                        wall.position.y - wall.size.y/2)) 
        elif wall.power_up == Wall.SNARE:
            screen.blit(wall_snare, (wall.position.x - wall.size.x/2, \
                        wall.position.y - wall.size.y/2)) 
        elif wall.power_up == Wall.DISARM:
            screen.blit(wall_disarm, (wall.position.x - wall.size.x/2, \
                        wall.position.y - wall.size.y/2)) 
        elif wall.power_up == Wall.VAMIPIRE:
            screen.blit(wall_vampire, (wall.position.x - wall.size.x/2, \
                        wall.position.y - wall.size.y/2))
        else:
            screen.blit(wall_image, (wall.position.x - wall.size.x/2, \
                        wall.position.y - wall.size.y/2))


def draw_players(game):
    players = (game.player_1, game.player_2)
    images = [player_1_image, player_2_image]
    for player, image in zip(players, images):
        if not player.alive:
            image = dead_player_image
        screen.blit(pygame.transform.rotate(image, get_leaning(player)), \
                    (player.position.x - player.size.x / 2, \
                     player.position.y - player.size.y / 2))


def render_game(game):
    screen.blit(background, (0, 0))
    draw_projectiles(game)    
    draw_players(game)
    draw_health(game)
    draw_walls(game)
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


def watch_sample_fight():
    if game.player_1.__class__ == tank.Tank:
        bot_1 = tank_bot.TankBot(game.player_1, game)
    else:
        bot_1 = berserker_bot.BerserkerBot(game.player_1, game)
    if game.player_2.__class__ == berserker.Berserker:
        bot_2 = berserker_bot.BerserkerBot(game.player_2, game)
    else:
        bot_2 = tank_bot.TankBot(game.player_2, game)

    while True:
        time_passed = clock.tick(FPS)
        bot_1.update(time_passed)
        bot_2.update(time_passed)
        game.update(bot_1.get_input(), bot_2.get_input(), time_passed)
        render_game(game)
        if game.winner is not None:
            break
    time.sleep(2)

def play_vs_human():
    while True:
        time_passed = clock.tick(FPS)
        game.update(controls.Controls.get_keyboard_input_player_1(),
                    controls.Controls.get_keyboard_input_player_2(),
                    time_passed)
        render_game(game)
        if game.winner is not None:
            break
    time.sleep(2)

def play_vs_computer():
    if game.player_2.__class__ == tank.Tank:
        bot = tank_bot.TankBot(game.player_2, game)
    else:
        bot = berserker_bot.BerserkerBot(game.player_2, game)

    while True:
        time_passed = clock.tick(FPS)
        bot.update(time_passed)
        game.update(controls.Controls.get_keyboard_input_player_1(), \
                    bot.get_input(), time_passed),
        render_game(game)
        if game.winner is not None:
            break
    time.sleep(2)
