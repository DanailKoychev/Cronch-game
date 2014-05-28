import game
import character

import random
import math

from game import *
import character

class Bot:
    def __init__(self, character, game):
        self.character = character
        self.game = game

        self.hidden = False
        self.wall_hiding_self = None

        if self.game.player_1 == character:
            self.enemy = self.game.player_2
        else:
            self.enemy = self.game.player_1

    # def spray():
    #     pass

    def get_approximate_own_projectile_flight_time(self):
        self.character.projectile_type.position = self.character.position
        return math.fabs(self.character.position.y - self.enemy.position.y) / \
               math.fabs(self.character.projectile_type.get_movement_vector(self.enemy.position ).y)

    def get_movement_range(self, character, time): 
        return (character.position.x - character.movement_speed * time, 
                character.position.x + character.movement_speed * time)

    def predict_enemy_position(self, time):
        expected_position_x = 0
        if self.enemy.state == MOVEING_LEFT:
            expected_position_x = self.enemy.position.x - \
                                  self.enemy_speed * time
        elif self.enemy.state == MOVING_RIGHT:
            expected_position_x = self.enemy.position.x + \
                                  self.enemy_speed * time
        else:
            expected_position_x = self.enemy_position.x

        if expected_position_x < self.enemy.size.x / 2:
            expected_position_x = self.enemy.size.x / 2
        elif expected_position_x > self.game.field_width - self.enemy.size.x / 2:
            expected_position_x = self.game.field_width - self.enemy.size.x / 2
        return expected_position_x

    def move_towards(self, point_x):
        if self.character.position.x > point_x:
            self.character.state = MOVING_LEFT
        elif self.character.position.x < point_x:
            self.character.state = MOVING_RIGHT
        else:
            self.character.state = STATIONARY

    def is_hidden(self):
        middle_point = self.character.position.x + self.enemy.position
        for wall in self.game.walls:
            if math.fabs(wall.position.x - middle_point) < WALL_LENGTH:
                return True
        return False

    def stay_hidden(self):
        safest_point = 2 * self.wall_hiding_self.position.x - self.enemy.position.x
        if math.fabs(self.character.position.x - safest_point) > \
           (self.character.speed * 1000) / Game.FPS:
            self.move_towards(safest_point)
        else:
            self.character.position.x = safest_point
        #if safest_point > 0 and safest_point < Game.FIELD_WIDTH:

#    def unhide(self):
 
    def get_closest_wall_to_reach(self):    # if the current closest wall is moving away it might not be the fastest one to reach
        closest_wall = None
        distance = Game.FIELD_WIDTH
        for wall in self.game.walls:
            if math.fabs(wall.position.x - self.character.position.x) < distance:
                distance = math.fabs(wall.position.x - self.character.position.x)
                closest_wall = wall
        return closest_wall

    # def move_away(self, projectile):
    #     if projectile.



