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
        self.wall_shield = None

        if self.game.player_1 == character:
            self.enemy = self.game.player_2
        else:
            self.enemy = self.game.player_1

    def get_approximate_own_projectile_flight_time(self):
        self.character.projectile_type.position = self.character.position
        return math.fabs(self.character.position.y - self.enemy.position.y) / \
               math.fabs(self.character.projectile_type.get_movement_vector(self.enemy.position ).y)

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
        enemy_movement_range = self.get_movement_range(self.enemy, self.get_approximate_own_projectile_flight_time())
        self.character.aim.x = random.randint(int(enemy_movement_range[0] + self.enemy.size.x), \
                                              int(enemy_movement_range[1] - self.enemy.size.x))
        self.character.try_shoot()

    def move_towards(self, point_x):
        if math.fabs(self.character.position.x - point_x) < \
           (self.character.speed * 1000) / Game.FPS:
           self.character.position.x = point_x
           self.state = STATIONARY
        elif self.character.position.x > point_x:
            self.character.state = MOVING_LEFT
        elif self.character.position.x < point_x:
            self.character.state = MOVING_RIGHT
        else:
            self.character.state = STATIONARY

    def move_away(self, point_x):
        if self.character.position.x <= point_x:
            self.character.state = MOVING_LEFT
        else:
            self.character.state = MOVING_RIGHT

    def is_hidden(self):
        middle_point = (self.character.position.x + self.enemy.position.x) / 2
        for wall in self.game.walls:
            if wall.position.x + wall.size[0] / 2 > middle_point and \
               wall.position.x - wall.size[0] / 2 < middle_point:
                self.wall_shield = wall   
                return True
        return False

    def hide(self):
        safest_point = 2 * self.wall_shield.position.x - self.enemy.position.x
        self.move_towards(safest_point)
        #if safest_point > 0 and safest_point < Game.FIELD_WIDTH:

#    def unhide(self):
 
    # def get_closest_wall_to_reach(self):    # if the current closest wall is moving away it might not be the fastest one to reach
    #     closest_wall = None
    #     distance = Game.FIELD_WIDTH
    #     for wall in self.game.walls:
    #         if math.fabs(wall.position.x - self.character.position.x) < distance:
    #             distance = math.fabs(wall.position.x - self.character.position.x)
    #             closest_wall = wall
    #     return closest_wall
    #     for wall in game.walls:



    # def get_projectile_destination_x(self, projectile):
    #     return (projectile.movement_vector.x / projectile.movement_vector.y) * \
    #             math.fabs(projectile.position.y - self.character.position.y) + \
    #             projectile.position.x

    def get_closest_wall(self):
        if not self.game.walls:
            return None
        return min([wall for wall in self.game.walls], \
                    key=lambda wall: math.fabs(wall.position.x - \
                    self.character.position.x))

    def dodge_projectiles(self):
        threats_from_left_count = 0
        threatening_projectiles = self.get_threatening_projectiles()
        for projectile in threatening_projectiles:
            if projectile.aim.x >= self.character.position.x:
                threats_from_left_count += 1
        if threats_from_left_count < len(threatening_projectiles) / 2:
            self.character.state = MOVING_RIGHT
        else:
            self.character.state = MOVING_LEFT

    def get_threatening_projectiles(self):
        return [projectile for projectile in self.enemy.active_projectiles \
                                             if self.is_threat(projectile)]

    def is_threat(self, projectile):
        if math.fabs(self.character.position.x - projectile.aim.x) < \
           self.character.size.x * 1.5:
           return True
        return False

    def defend(self):
        self.wall_shield = self.get_closest_wall()
        if not self.is_hidden() and len(self.get_threatening_projectiles()) > 0:
            self.dodge_projectiles()
        elif self.wall_shield != None:
            self.hide()
        else:
            self.character.state = STATIONARY
         





    # def get_danger_projectiles():
    #     return [projectile for projectile in self.enemy.active_projectiles \
    #             if abs(projectile.y - self.character.y) < ]



    # def move_away(self, projectile):
    #     if projectile.



