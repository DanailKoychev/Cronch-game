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

    FPS = 120

    PVE = 0
    PVP = 1

    def __init__(self, game_mode=PVE):
        if game_mode == Game.PVE:
            Game.init_sample_PVE_1v1(self)
        elif game_mode == Game.PVP:
            raise NotImplementedError("no pvp yet")

        self.time_since_last_wall = 0
        self.Clock = Clock()

    #def init_PVE_1v1(self, character_type_1, character_type_2):
    # 

    def init_sample_PVE_1v1(self):
        projectile_type = Projectile(Point(50, 50), Point(10, 10), 1, 5, Point(0, 0))        
        self.player_1 = Character(Point(400, 550), \
                        Point(60, 60), 0.4, 300, projectile_type, 50, 5, 0.7)
        self.player_2 = Character(Point(400, 50), \
                        Point(60, 60), 0.4, 300, projectile_type, 50, 5, 0.7)
        self.walls = []

    def get_all_players_input(self):
        players_input = zip(self.human_players, 
                        [get_keyboard_input() for player in self.human_players])
        return players_input

    def collide(self, object_one, object_two):
        if math.fabs(object_one.position.x - object_two.position.x) < \
           object_one.size.x / 2 + object_two.size.x / 2 and \
           math.fabs(object_one.position.y - object_two.position.y) < \
           object_one.size.y / 2 + object_two.size.y / 2:
            return True
        return False

    def update(self, instrucions_player_1, instrucions_player_2):
        time_passed = self.Clock.tick(Game.FPS)

        for player, instruction_set in ((self.player_1, instrucions_player_1),\
                                       (self.player_2, instrucions_player_2)):
            player.use_input(instruction_set, time_passed)
            if player.position.x  + player.size.x / 2 > Game.FIELD_WIDTH:
               player.position.x = Game.FIELD_WIDTH - player.size.x / 2
            if player.position.x - player.size.x / 2 < 0:
               player.position.x = player.size.x / 2;
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

                for pl in (self.player_1, self.player_2):
                    if pl != player and self.collide(projectile, pl):
                        pl.get_hit(projectile)
                        player.active_projectiles.remove(projectile)
            # for player in self.ai_players:
        #     player.update(time_passed) 

        for wall in self.walls:
            if wall.position.x < 0 - wall.size.x:
                self.walls.remove(wall)
            else:
                wall.update(time_passed)

        self.time_since_last_wall -= time_passed
        if self.time_since_last_wall <= 0:
            self.time_since_last_wall = randint(Game.WALL_SPAWN_TIME_RANGE[0], \
                                                Game.WALL_SPAWN_TIME_RANGE[1])
            self.walls.append(Wall(Point(100, 5), False, Game.FIELD_WIDTH, Game.FIELD_HEGHT))

        # if time_passed > 18:
        #     print("FAK UU GUBIIII")
