from projectile import *
from character import *
from input_getter import *
import itertools
import math
from random import randint

from pygame.time import Clock

class Game:
    FIELD_HEGHT = 600
    FIELD_WIDTH = 800
    WALL_SPAWN_TIME_RANGE = (3000, 7000)


    FPS = 60

    def __init__(self, game_mode=0): # use enum for modes
        if game_mode == 0:
            Game.init_PVE_1v1(self)
        # elif game mode = ...

        self.time_since_last_wall = 0
        self.Clock = Clock()

    def init_PVE_1v1(self):
        #----------------
        self.player_1 = Character(Point(400, 550), Point(60, 60), 0.4, 300, Projectile(Point(50, 50), [10, 10], 1, 0, Point(0, 0)), 50, 5, 0.7)
        self.player_2 = Character(Point(400, 50), Point(60, 60), 0.4, 300, Projectile(Point(50, 50), [10, 10], 1, 0, Point(0, 0)), 50, 5, 0.7)
        #----------------

        self.human_players = (self.player_1,)
        self.ai_players = (self.player_2,)
        self.walls = []

    def get_all_players_input(self):
        players_input = zip(self.human_players, 
                        [get_keyboard_input() for player in self.human_players])
        return players_input

    def collide(self, object_one, object_two):
        if math.fabs(object_one.position.x - object_two.position.x) < \
           object_one.size[0] / 2 + object_two.size[0] / 2 and \
           math.fabs(object_one.position.y - object_two.position.y) < \
           object_one.size[1] / 2 + object_two.size[1] / 2:
            return True
        return False

    def update(self):
        time_passed = self.Clock.tick(Game.FPS)
        for player, instrucions in self.get_all_players_input():
            if MOVE_LEFT in instrucions:
                player.state = MOVING_LEFT
            elif MOVE_RIGHT in instrucions:
                player.state = MOVING_RIGHT
            else:
                player.state = STATIONARY

            if USE_SKILL in instrucions:
                # not implemented
                pass
            if AIM_LEFT in instrucions:
                player.move_aim_left(time_passed)
            if AIM_RIGHT in instrucions:
                player.move_aim_right(time_passed)
            if SHOOT in instrucions:
                player.try_shoot()

        for player in (self.player_1, self.player_2):
            player.update(time_passed)
            for projectile in player.active_projectiles:
                if (projectile.position.y < 0 or projectile.position.y > Game.FIELD_HEGHT):
                    player.active_projectiles.remove(projectile)
                else:
                    projectile.update(time_passed)
                    if projectile.position.x < 0:
                        projectile.reflect_horizontally(0)
                    elif projectile.position.x > Game.FIELD_WIDTH:
                        projectile.reflect_horizontally(Game.FIELD_WIDTH)

            for projectile in player.active_projectiles:
                for wall in self.walls:
                    if self.collide(projectile, wall):
                        player.active_projectiles.remove(projectile)
        # for player in self.ai_players:
        #     player.update(time_passed) 

        for wall in self.walls:
            if wall.position.x < 0 - wall.size[0]:
                self.walls.remove(wall)
            else:
                wall.update(time_passed)

        self.time_since_last_wall -= time_passed
        if self.time_since_last_wall <= 0:
            self.time_since_last_wall = randint(Game.WALL_SPAWN_TIME_RANGE[0], \
                                                Game.WALL_SPAWN_TIME_RANGE[1])
            self.walls.append(Wall((100, 5), False, Game.FIELD_WIDTH, Game.FIELD_HEGHT))

        # if time_passed > 18:
        #     print("FAK UU GUBIIII")
