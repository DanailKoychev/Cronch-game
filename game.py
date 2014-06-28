from itertools import product
import math
from random import randint

#from pygame.time import Clock

from projectile import *
from character import *
from controls import *
from berserker import *
from tank import *

class Game: 
    FIELD_HEIGHT = 600
    FIELD_WIDTH = 800
    WALL_SPAWN_TIME_RANGE = (2400, 5900)
    POWER_UP_SPAWN_TIME_RANGE = (4800, 7300)

    FPS = 120

    PVE = 0
    PVP = 1
 
    def __init__(self, game_mode=PVE):
        if game_mode == Game.PVE:
            Game.init_sample_PVE_1v1(self)
        elif game_mode == Game.PVP:
            raise NotImplementedError("no pvp yet")

        self.field_width = Game.FIELD_WIDTH
        self.field_height = Game.FIELD_HEIGHT
        self.time_since_last_wall = 0
        self.time_since_last_power_up = randint(
                                            self.POWER_UP_SPAWN_TIME_RANGE[0],
                                            self.POWER_UP_SPAWN_TIME_RANGE[1]
                                            )
   #     self.Clock = Clock()

    #def init_PVE_1v1(self, character_type_1, character_type_2):
    # 

    def init_sample_PVE_1v1(self):
        projectile_type = Projectile(Point(50, 50), Point(10, 10), 1, 5, Point(0, 0))        
       # self.player_1 = Berserker(Point(400, 550))
        self.player_1 = Tank(Point(400, 520))
        self.player_1.aim = Point(400, 0)
        self.player_2 = Berserker(Point(400, 80))#, \
                        #Point(60, 60), 0.4, 300, projectile_type, 50, 5)
        self.player_2.aim = Point(400, 600)

        self.walls = []

        self.active_projectiles = []

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

    def use_input(self, player, instruction_set, time_passed):
            if MOVE_LEFT in instruction_set:
                player.move_left(time_passed)
            elif MOVE_RIGHT in instruction_set:
                player.move_right(time_passed)
            if USE_SKILL in instruction_set:
                player.use_skill()
            if AIM_LEFT in instruction_set:
                player.move_aim_left(time_passed)
            if AIM_RIGHT in instruction_set:
                player.move_aim_right(time_passed)
            if SHOOT in instruction_set:
                shot = player.try_shoot()
                if shot is not None:
                    self.active_projectiles.append(shot)

    def update(self, instrucions_player_1, instrucions_player_2, time_passed):
        #time_passed = self.Clock.tick(Game.FPS)

        for player, instruction_set in ((self.player_1, instrucions_player_1),\
                                       (self.player_2, instrucions_player_2)):
            self.use_input(player, instruction_set, time_passed)
            
        self.handle_player_hits()
        self.handle_wall_collisions()
        self.update_players(time_passed)
        self.update_projectiles(time_passed)
        self.update_walls(time_passed)
        self.manage_wall_spawning(time_passed)
        self.manage_power_ups(time_passed)

    def update_players(self, time_passed):
        for player in (self.player_1, self.player_2):
            if player.x  + player.size.x / 2 > self.field_width:
               player.x = self.field_width - player.size.x / 2
            if player.x - player.size.x / 2 < 0:
               player.x = player.size.x / 2;
            player.update(time_passed)

            if player.aim.x < - self.field_height / 3:
                player.aim.x = - self.field_height / 3
            if player.aim.x > self.field_width + self.field_height / 3:
                player.aim.x = self.field_width + self.field_height / 3

            for projectile in player.own_projectiles:
                if projectile not in self.active_projectiles:
                    player.own_projectiles.remove(projectile)

    def handle_player_hits(self):
        for player, projectile in product((self.player_1, self.player_2), \
                                           self.active_projectiles):
            if projectile not in player.own_projectiles and \
               self.collide(projectile, player):
                player.get_hit(projectile)
                self.active_projectiles.remove(projectile)

                if projectile.owner.vampire == True:
                    projectile.owner.health += projectile.damage * (VAMPIRE_PERCENT / 100)

    def handle_wall_collisions(self):
        for projectile, wall in product(self.active_projectiles, self.walls):
            if self.collide(projectile, wall):
                self.active_projectiles.remove(projectile)

                if wall.power_up == HEAL:
                    projectile.owner.health += HEAL_VALUE
                elif wall.power_up == SPEED_UP:
                    projectile.owner.speed *= 1 + (SPEED_UP_PERCENT / 100)
                elif wall.power_up == VAMIPIRE:
                    projectile.owner.vampire = True
                    projectile.owner.vampire_time_left = VAMPIRE_TIME
                elif wall.power_up == DISARM:
                    if projectile.owner == self.player_1:
                        self.player_2.disarmed = True
                        self.player_2.disarm_time_left = DISARM_TIME_MILLISEC
                    else:
                        self.player_1.disarmed = True
                        self.player_1.disarm_time_left = DISARM_TIME_MILLISEC
                elif wall.power_up == SNARE:
                    if projectile.owner == self.player_1:
                        self.player_2.snared = True
                        self.player_2.snare_time_left = SNARE_TIME_MILLISEC
                    else:
                        self.player_1.snared = True
                        self.player_1.snare_time_left = SNARE_TIME_MILLISEC
                wall.power_up = None

    def manage_wall_spawning(self, time_passed):
        self.time_since_last_wall -= time_passed
        if self.time_since_last_wall <= 0:
            self.time_since_last_wall = randint(Game.WALL_SPAWN_TIME_RANGE[0], \
                                                Game.WALL_SPAWN_TIME_RANGE[1])
            self.walls.append(Wall(Point(100, 5), False, self.field_width, \
                                   self.field_height))

    def manage_power_ups(self, time_passed):
        self.time_since_last_power_up -= time_passed
        if self.time_since_last_power_up <= 0:
            self.walls[randint(0, len(self.walls) - 1)].power_up = randint(0, 4)
            self.time_since_last_power_up = randint(
                                            self.POWER_UP_SPAWN_TIME_RANGE[0],
                                            self.POWER_UP_SPAWN_TIME_RANGE[1]
                                            )

    def update_projectiles(self, time_passed):
       for projectile in self.active_projectiles:
            if projectile.y < 0 or projectile.y > self.field_height:
                self.active_projectiles.remove(projectile)
            if projectile.x < 0:
                projectile.reflect_horizontally(0)
            elif projectile.x > self.field_width:
                projectile.reflect_horizontally(self.field_width)
            projectile.update(time_passed)

    def update_walls(self, time_passed):
        for wall in self.walls:
            if wall.x < 0 - wall.size.x:
                self.walls.remove(wall)
            else:
                wall.update(time_passed)