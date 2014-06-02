import game
import character

import input_getter
import random
import math

from game import *
import character

class Bot:
    def __init__(self, character, game):
        self.character = character
        self.game = game

        self.hidden = False
        self.wall_shield = None

        if self.game.player_1 == character:
            self.enemy = self.game.player_2
        else:
            self.enemy = self.game.player_1

        self.character.aim.y = self.enemy.position.y

    def get_projectile_flight_time(projectile, point_1, point_2):
        projectile.position = point_1
        return math.fabs(point_1.y - point_2.y) /\
               math.fabs(projectile.get_movement_vector(point_2).y)

    def get_movement_range(self, character, time): 
        return (character.position.x - character.speed * time, 
                character.position.x + character.speed * time)

    def predict_enemy_position(self, time):
        expected_position_x = 0
        if self.enemy.state == MOVING_LEFT:
            expected_position_x = self.enemy.position.x - \
                                  self.enemy.speed * time
        elif self.enemy.state == MOVING_RIGHT:
            expected_position_x = self.enemy.position.x + \
                                  self.enemy.speed * time
        else:
            expected_position_x = self.enemy.position.x

        if expected_position_x < self.enemy.size.x / 2:
            expected_position_x = self.enemy.size.x / 2
        elif expected_position_x > Game.FIELD_WIDTH - self.enemy.size.x / 2:
            expected_position_x = Game.FIELD_WIDTH - self.enemy.size.x / 2
        return expected_position_x

    def spray_projectiles(self):
        if self.character.ready_to_shoot:
            enemy_movement_range = self.get_movement_range(self.enemy, \
                                   Bot.get_projectile_flight_time(self.character.projectile_type, self.character.position, self.enemy.position))
            self.character.aim.x = random.randint(int(enemy_movement_range[0] + self.enemy.size.x), \
                                              int(enemy_movement_range[1] - self.enemy.size.x))
        return input_getter.SHOOT

    def move_towards(self, point_x):
        if self.character.position.x > point_x:
            return input_getter.MOVE_LEFT
        elif self.character.position.x < point_x:
            return input_getter.MOVE_RIGHT

    def move_away(self, point_x):
        if self.character.position.x <= point_x:
            return input_getter.MOVE_LEFT
        else:
            return input_getter.MOVE_RIGHT

    def is_hidden(self):
        middle_point = (self.character.position.x + self.enemy.position.x) / 2
        for wall in self.game.walls:
            if wall.position.x + wall.size.x / 2 > middle_point and \
               wall.position.x - wall.size.x / 2 < middle_point:
                self.wall_shield = wall   
                return True
        return False

    def hide(self):
        safest_point = 2 * self.wall_shield.position.x - self.enemy.position.x
        return self.move_towards(safest_point)


    def get_closest_wall(self):
        if self.game.walls:
            return min([wall for wall in self.game.walls], \
                    key=lambda wall: math.fabs(wall.position.x - \
                    self.character.position.x))

    def dodge_projectiles(self):
        threats_from_left_count = 0
        threatening_projectiles = self.get_threatening_projectiles()
        if self.character.position.x < 1.5 * self.character.size.x:
            return input_getter.MOVE_RIGHT
        if self.character.position.x > \
           Game.FIELD_WIDTH - 1.5 * self.character.size.x:
            return input_getter.MOVE_LEFT
        for projectile in threatening_projectiles:
            if projectile.aim.x >= self.character.position.x:
                threats_from_left_count += 1
        if threats_from_left_count < len(threatening_projectiles) / 2:
            return input_getter.MOVE_RIGHT
        elif threats_from_left_count > len(threatening_projectiles) / 2:
            return input_getter.MOVE_LEFT

    def get_threatening_projectiles(self):
        return [projectile for projectile in self.enemy.active_projectiles \
                                             if self.is_threat(projectile)]

    def is_threat(self, projectile):
        if math.fabs(self.character.position.x - projectile.aim.x) < \
           self.character.size.x * 1.5:
           return True
        return False

    def move_randomly(self):
        move = random.randint(0,2)
        if move == 0:
            return input_getter.MOVE_LEFT
        elif move == 2:
            return input_getter.MOVE_RIGHT

    def defend(self):
        movement_instructions = []
        self.wall_shield = self.get_closest_wall()
        if len(self.get_threatening_projectiles()) > 0:
            movement_instructions.append(self.dodge_projectiles())
        elif self.wall_shield != None:  
            movement_instructions.append(self.hide())
        return movement_instructions

    def get_input(self):
        # return [self.move_randomly()]

        instructions = self.defend()
        instructions.append(self.spray_projectiles())
        return instructions


    #def snipe()
    # formula: self.character.aim.x = self.predict_enemy_position(self.get_approximate_own_projectile_flight_time())