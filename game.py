from projectile import *
from character import *
from input_getter import *
import itertools

class Game:
    FIELD_HEGHT = 600
    FIELD_WIDTH = 800

    def __init__(self, game_mode=0): # use enum for modes
        if game_mode == 0:
            Game.init_PVE_1v1(self)
        # elif game mode = ...

    def init_PVE_1v1(self):
        #----------------
        self.player_1 = Character(Point(400, 480), Point(60, 60), 0.4, 300, Projectile(Point(50, 50), [10, 10], 1, 0), 50, 5, 0.7)
        self.player_2 = Character(Point(400, 20), Point(60, 60), 0.4, 300, Projectile(Point(50, 50), [10, 10], 1, 0), 50, 5, 0.7)
        #----------------

        self.human_players = (self.player_1,)
        self.ai_players = (self.player_2,)
        self.walls = []

    def get_all_players_input(self):
        players_input = zip(self.human_players, 
                        [get_keyboard_input() for player in self.human_players])
        return players_input

    def update(self, time_passed):
        for player, instrucions in self.get_all_players_input():
            if MOVE_LEFT in instrucions:
                player.move_left(time_passed)
            if MOVE_RIGHT in instrucions:
                player.move_righ(time_passed)
            if USE_SKILL in instrucions:
                # not implemented
                pass
            if AIM_LEFT in instrucions:
                player.move_aim_left(time_passed)
            if AIM_RIGHT in instrucions:
                player.move_aim_right(time_passed)
            if SHOOT in instrucions:
                player.try_shoot(time_passed)
            player.update(time_passed)

            print(len(self.player_1.active_projectiles))

        for projectile in itertools.chain(self.player_1.active_projectiles,
                                          self.player_2.active_projectiles):
            if (projectile.position.y < 0 or projectile.position.y > Game.FIELD_HEGHT):
                player.active_projectiles.remove(projectile)
            else:
                projectile.update(time_passed)
                if projectile.position.x < 0:
                    projectile.reflect_horizontally(0)
                elif projectile.position.x > Game.FIELD_WIDTH:
                    projectile.reflect_horizontally(Game.FIELD_WIDTH)

        for player in self.ai_players:
            # do ai stuff
            player.update(time_passed) 

        for wall in self.walls:  
            wall.update(time_passed)