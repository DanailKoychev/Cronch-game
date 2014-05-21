import game
import character

import random
import math

class Bot:
    def __init__(self, character, game):
        self.character = character
        self.game = game
        if self.game.player_1 == character:
            self.enemy = self.game.player_2
        else:
            self.enemy = self.game.player_1

    # def spray():
    #     pass

    def get_approximate_projectile_fight_time(self):
        self.character.projectile_type.position = self.character.position
        return math.fabs(self.character.position.y - self.enemy.position.y) / \
               math.fabs(self.player_1.projectile_type.get_movement_vector(self.player_1.aim).y)

    def get_enemy_movement_range(self, time): 
        return (self.enemy.position.x - self.enemy.movement_speed * time, 
                self.enemy.position.x + self.enemy.movement_speed * time)

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

        if expected_position_x < 0:
            expected_position_x = 0
        elif expected_position_x > self.game.field_width:
            expected_position_x = self.game.field_width
        return expected_position_x
