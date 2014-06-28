from itertools import product
import math
from random import randint

from point import *
from projectile import *
from character import *
from controls import *
from berserker import *
from tank import *
from wall import *

class Game: 
    FIELD_HEIGHT = 600
    FIELD_WIDTH = 800
    WALL_SPAWN_TIME_RANGE = (2400, 5900)
    POWER_UP_SPAWN_TIME_RANGE = (4800, 7300)

    character_types = ["no_type", "tank", "berserker"]
 
    def __init__(self, player_1_type="no_type", player_2_type="no_type"):
        self.field_width = Game.FIELD_WIDTH
        self.field_height = Game.FIELD_HEIGHT
        self.time_to_next_wall = 0
        self.time_to_next_power_up = randint(
                                            self.POWER_UP_SPAWN_TIME_RANGE[0],
                                            self.POWER_UP_SPAWN_TIME_RANGE[1]
                                            )
        player_1_position = Point(self.field_width / 2, self.field_height  * 7 / 8)
        player_2_position = Point(self.field_width / 2, self.field_width / 8)

        self.player_1 = Game.create_character(player_1_position, player_1_type)
        self.player_1.aim = Point(player_2_position.x, player_2_position.y)
        self.player_2 = Game.create_character(player_2_position, player_2_type)
        self.player_2.aim = Point(player_1_position.x, player_1_position.y)
        self.walls = []
        self.active_projectiles = []
        self.winner = None

    def create_character(position, character_type):
        if character_type == "berserker":
            return Berserker(position)
        elif character_type == "tank":
            return Tank(position)

    def collide_rectangles(object_one, object_two):
        if math.fabs(object_one.position.x - object_two.position.x) < \
           object_one.size.x / 2 + object_two.size.x / 2 and \
           math.fabs(object_one.position.y - object_two.position.y) < \
           object_one.size.y / 2 + object_two.size.y / 2:
            return True
        return False

    def collide_circles(object_one, object_two):
        return math.sqrt(
            math.fabs(object_one.position.x - object_two.position.x) ** 2 + \
            math.fabs(object_one.position.y - object_two.position.y) ** 2) < \
            (object_one.size.y + object_two.size.y) / 2

    def use_input(self, player, instruction_set, time_passed):
            if Controls.MOVE_LEFT in instruction_set:
                player.move_left(time_passed)
            elif Controls.MOVE_RIGHT in instruction_set:
                player.move_right(time_passed)
            if Controls.USE_SKILL in instruction_set:
                player.use_skill()
            if Controls.AIM_LEFT in instruction_set:
                player.move_aim_left(time_passed)
            if Controls.AIM_RIGHT in instruction_set:
                player.move_aim_right(time_passed)
            if Controls.SHOOT in instruction_set:
                shot = player.try_shoot()
                if shot is not None:
                    self.active_projectiles.append(shot)

    def update(self, instrucions_player_1, instrucions_player_2, time_passed):
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

        if not self.player_1.alive:
            self.winner = self.player_2
        elif not self.player_2.alive:
            self.winner = self.player_1

    def update_players(self, time_passed):
        for player in (self.player_1, self.player_2):
            if player.x  + player.size.x / 2 > self.field_width:
               player.x = self.field_width - player.size.x / 2
            if player.x - player.size.x / 2 < 0:
               player.x = player.size.x / 2;
            player.update(time_passed)

            if player.aim.x < - self.field_width / 2:
                player.aim.x = - self.field_width / 2
            if player.aim.x > self.field_width + self.field_height / 3:
                player.aim.x = self.field_width + self.field_height / 3

            for projectile in player.own_projectiles:
                if projectile not in self.active_projectiles:
                    player.own_projectiles.remove(projectile)

    def handle_player_hits(self):
        for player, projectile in product((self.player_1, self.player_2), \
                                           self.active_projectiles):
            if projectile not in player.own_projectiles and \
               Game.collide_circles(projectile, player):
                player.get_hit(projectile)
                self.active_projectiles.remove(projectile)

                if projectile.owner.vampire == True:
                    projectile.owner.health += projectile.damage * (VAMPIRE_PERCENT / 100)

    def handle_wall_collisions(self):
        for projectile, wall in product(self.active_projectiles, self.walls):
            if Game.collide_rectangles(projectile, wall):
                self.active_projectiles.remove(projectile)

                if wall.power_up == Wall.HEAL:
                    projectile.owner.health += HEAL_VALUE
                elif wall.power_up == Wall.SPEED_UP:
                    projectile.owner.speed *= 1 + (SPEED_UP_PERCENT / 100)
                elif wall.power_up == Wall.VAMIPIRE:
                    projectile.owner.vampire = True
                    projectile.owner.vampire_time_left = VAMPIRE_TIME
                elif wall.power_up == Wall.DISARM:
                    if projectile.owner == self.player_1:
                        self.player_2.disarmed = True
                        self.player_2.disarm_time_left = DISARM_TIME_MILLISEC
                    else:
                        self.player_1.disarmed = True
                        self.player_1.disarm_time_left = DISARM_TIME_MILLISEC
                elif wall.power_up == Wall.SNARE:
                    if projectile.owner == self.player_1:
                        self.player_2.snared = True
                        self.player_2.snare_time_left = SNARE_TIME_MILLISEC
                    else:
                        self.player_1.snared = True
                        self.player_1.snare_time_left = SNARE_TIME_MILLISEC
                wall.power_up = None

    def manage_wall_spawning(self, time_passed):
        self.time_to_next_wall -= time_passed
        if self.time_to_next_wall <= 0:
            self.time_to_next_wall = randint(Game.WALL_SPAWN_TIME_RANGE[0], \
                                                Game.WALL_SPAWN_TIME_RANGE[1])
            self.walls.append(Wall(Point(100, 5), False, self.field_width, \
                                   self.field_height))

    def manage_power_ups(self, time_passed):
        self.time_to_next_power_up -= time_passed
        if self.time_to_next_power_up <= 0:
            self.walls[randint(0, len(self.walls) - 1)].power_up = randint(0, 4)
            self.time_to_next_power_up = randint(
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
