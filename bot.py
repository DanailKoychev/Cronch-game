import random
import math

import character
import controls
from game import *
import character

class Bot:
    def __init__(self, character, game):
        self.character = character
        self.game = game
        self.wall_shield = None
        self.time_until_behavior_change = 0
        self.defensive = False

        if self.game.player_1 == character:
            self.enemy = self.game.player_2
        else:
            self.enemy = self.game.player_1

        self.character.aim.y = self.enemy.y

    def get_projectile_flight_time(projectile, point_1, point_2):
        initial_projectile_position = projectile.position
        projectile.position = point_1
        flight_time = math.fabs(point_1.y - point_2.y) /\
               math.fabs(projectile.get_movement_vector(point_2).y)
        projectile.position = initial_projectile_position
        return flight_time

    def get_movement_range(self, character, time): 
        return (character.x - character.speed * time, 
                character.x + character.speed * time)

    def predict_enemy_position(self, time):
        expected_position_x = 0
        if self.enemy.state == MOVING_LEFT:
            expected_position_x = self.enemy.x - \
                                  self.enemy.speed * time
        elif self.enemy.state == MOVING_RIGHT:
            expected_position_x = self.enemy.x + \
                                  self.enemy.speed * time
        else:
            expected_position_x = self.enemy.x

        if expected_position_x < self.enemy.size.x / 2:
            expected_position_x = self.enemy.size.x / 2
        elif expected_position_x > self.game.field_width - self.enemy.size.x / 2:
            expected_position_x = self.game.field_height - self.enemy.size.x / 2
        return expected_position_x

    def spray_projectiles(self):
        if self.character.ready_to_shoot:
            enemy_movement_range = self.get_movement_range(self.enemy, \
                                   Bot.get_projectile_flight_time( \
                                   self.character.projectile_type, \
                                   self.character.position, self.enemy.position))
            self.character.aim.x = random.randint( \
                            int(enemy_movement_range[0]),\
                            int(enemy_movement_range[1]))
                            #int(enemy_movement_range[0] + self.enemy.size.x),\
                            #int(enemy_movement_range[1] - self.enemy.size.x))
            return controls.Controls.SHOOT

    def snipe(self):
        if self.character.ready_to_shoot:
            self.character.aim.x = self.enemy.x
            return controls.Controls.SHOOT

    def manage_shooting(self):
        if not self.is_hidden() and not self.character.disarmed:
            if self.enemy.snared:
                return self.snipe()
            else:
                return self.spray_projectiles()

    def move_towards(self, point_x):
        if self.character.x > point_x:
            return controls.Controls.MOVE_LEFT
        elif self.character.x < point_x:
            return controls.Controls.MOVE_RIGHT

    def move_away(self, point_x):
        if self.character.x <= point_x:
            return controls.Controls.MOVE_LEFT
        else:
            return controls.Controls.MOVE_RIGHT

    def is_hidden(self):
        middle_point_between_characters = (self.character.x + self.enemy.x) / 2
        for wall in self.game.walls:
            if wall.x + wall.size.x / 2 > middle_point_between_characters and\
               wall.x - wall.size.x / 2 < middle_point_between_characters:
                self.wall_shield = wall   
                return True
        return False

    def hide(self):
        safest_point = 2 * self.wall_shield.position.x - self.enemy.x
        if safest_point > self.game.field_width / 10 and \
           safest_point < self.game.field_width * 11 / 10:
            return self.move_towards(safest_point)
        else:
            return self.move_away(safest_point)

    def unhide(self):
        safest_point = 2 * self.wall_shield.position.x - self.enemy.x
        return self.move_away(safest_point)

    def get_closest_wall(self):
        if self.game.walls:
            return min([wall for wall in self.game.walls], \
                    key=lambda wall: math.fabs(wall.x - \
                    self.character.x))

    def dodge_projectiles(self):
        threats_from_left_count = 0
        threatening_projectiles = self.get_threatening_projectiles()
        for projectile in threatening_projectiles:
            if projectile.aim.x >= self.character.x:
                threats_from_left_count += 1
        if threats_from_left_count < len(threatening_projectiles) / 2:
            return controls.Controls.MOVE_RIGHT
        elif threats_from_left_count > len(threatening_projectiles) / 2:
            return controls.Controls.MOVE_LEFT

    def get_threatening_projectiles(self):
        return [projectile for projectile in self.enemy.own_projectiles \
                                             if self.is_threat(projectile)]

    def is_threat(self, projectile):
        if math.fabs(self.character.x - projectile.aim.x) < \
           self.character.size.x * 1.5:
           return True
        return False

    def offence(self):
        movement_instructions = []
        self.wall_shield = self.get_closest_wall()
        if len(self.get_threatening_projectiles()) > 0:
            movement_instructions.append(self.dodge_projectiles())
        elif self.wall_shield != None:  
            movement_instructions.append(self.unhide())
        return movement_instructions

    def defence(self):
        movement_instructions = []
        self.wall_shield = self.get_closest_wall()
        if len(self.get_threatening_projectiles()) > 0:
            movement_instructions.append(self.dodge_projectiles())
        elif self.wall_shield != None:  
            movement_instructions.append(self.hide())
        return movement_instructions

    def get_input(self):
        if self.character.disarmed or self.enemy.vampire:
            instructions = self.defence()
        elif self.character.vampire or self.enemy.snared or self.enemy.disarmed:
            instructions = self.offence()
        instructions = self.follow_default_behavior()
        instructions.append(self.manage_shooting())
        return instructions

    def follow_default_behavior(self):
        instructions = []
        if self.defensive:
            instructions = self.defence()
        else:
            instructions = self.offence()
        return instructions

    def update(self, time_passed):
        self.time_until_behavior_change -= time_passed
        if self.time_until_behavior_change <= 0:
            self.time_until_behavior_change = random.randint(700, 3000)
            if random.randint(0, 1):
                self.defensive = True;
            else:
                self.defensive = False

        # if self.is_hidden():
        #     print("dsfjusghuhsdfaglasdfgkjasdkjgn")