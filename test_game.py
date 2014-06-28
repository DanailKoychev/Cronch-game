import unittest

import point
import game
import projectile
import character
import controls
import berserker
import tank
import wall

class GameTest(unittest.TestCase):
    def test_collide_rectangles(self):
        object_one = projectile.Projectile(point.Point(20, 20),
                                           point.Point(20, 20),
                                           None, None, point.Point(0,0))
        object_two = projectile.Projectile(point.Point(39, 40),
                                           point.Point(20, 20),
                                           None, None, point.Point(0,0))
        self.assertFalse(game.Game.collide_rectangles(object_one, object_two))
        object_three = projectile.Projectile(point.Point(39, 39),
                                           point.Point(20, 20),
                                           None, None, point.Point(0,0))
        self.assertTrue(game.Game.collide_rectangles(object_one, object_three))

    def test_collide_circles(self):
        object_one = projectile.Projectile(point.Point(20, 20),
                                           point.Point(20, 20),
                                           None, None, point.Point(0,0))
        object_two = projectile.Projectile(point.Point(39, 40),
                                           point.Point(20, 20),
                                           None, None, point.Point(0,0))
        self.assertFalse(game.Game.collide_rectangles(object_one, object_two))
        object_three = projectile.Projectile(point.Point(39, 39),
                                           point.Point(20, 20),
                                           None, None, point.Point(0,0))
        self.assertTrue(game.Game.collide_rectangles(object_one, object_three))

    def test_use_input(self):
        sample_game = game.game = game.Game("tank", "berserker")
        instruction_set = [controls.Controls.MOVE_LEFT,
                           controls.Controls.SHOOT]
        time_passed = 15
        player_1_x = sample_game.player_1.x
        sample_game.use_input(sample_game.player_1, instruction_set, time_passed)
        self.assertEqual(player_1_x - 15 * sample_game.player_1.speed,
                         sample_game.player_1.x)
        self.assertIn(sample_game.player_1.own_projectiles[0],
                      sample_game.active_projectiles)

        instruction_set = [controls.Controls.AIM_RIGHT]
        player_1_aim_x = sample_game.player_1.aim.x
        sample_game.use_input(sample_game.player_1, instruction_set, time_passed)
        self.assertEqual(player_1_aim_x + 15 * character.Character.AIM_SPEED,
                         sample_game.player_1.aim.x)

    def test_update_players(self):
        sample_game = game.game = game.Game("tank", "berserker")
        time_passed = 20
        player = sample_game.player_1
        sample_game.player_1.x = -15
        sample_game.update_players(time_passed)
        self.assertEqual(player.x, player.size.x / 2)
        player.aim.x = - sample_game.field_width * 3
        sample_game.update_players(time_passed)
        self.assertEqual(player.aim.x, - sample_game.field_width / 2)
        player.own_projectiles = ["not_actual_projectile", "not_projectile"]
        sample_game.update_players(time_passed)
        self.assertNotIn(player.own_projectiles[0], 
            sample_game.active_projectiles)

    def test_handle_player_hits(self):
        sample_game = game.game = game.Game("tank", "berserker")
        player = sample_game.player_1
        projectile = player.projectile_type
        projectile.owner = player
        player.health = 0
        projectile.damage = 10
        player.x, player.y = 10, 10
        sample_game.active_projectiles.append(projectile)
        projectile.position.x = 10
        projectile.position.y = 10
        sample_game.handle_player_hits()
        self.assertEqual(player.health, -10)
        self.assertNotIn(projectile, sample_game.active_projectiles)

        player.health = 13
        sample_game.active_projectiles.append(projectile)
        player.own_projectiles.append(projectile)
        sample_game.handle_player_hits()
        self.assertEqual(player.health, 13)

    def test_manage_wall_spawning(self):
        sample_game = game.game = game.Game("tank", "berserker")
        sample_game.walls = []
        sample_game.time_to_next_wall = 0
        time_passed = 0
        sample_game.manage_wall_spawning(time_passed)
        self.assertEqual(len(sample_game.walls), 1)

    def test_manage_power_ups(self):
        sample_game = game.game = game.Game("tank", "berserker")
        sample_game.walls = [wall.Wall(point.Point(10, 10), False, 100, 100)]
        sample_game.time_to_next_power_up = 0
        time_passed = 0
        sample_game.manage_power_ups(time_passed)
        self.assertNotEqual(sample_game.walls[0].power_up, None)       

    def test_update_projectiles(self):
        sample_game = game.game = game.Game("tank", "berserker")
        sample_projectile = projectile.Projectile(point.Point(-100, -100),
                                           point.Point(0, 0), 5, 5,
                                           point.Point(-1, 0))
        sample_game.active_projectiles.append(sample_projectile)
        time_passed = 20
        sample_game.update_projectiles(time_passed)
        self.assertEqual(len(sample_game.active_projectiles), 0)
        sample_game.active_projectiles.append(sample_projectile)
        sample_projectile.position = point.Point(-10, 10)
        sample_projectile.speed = 0
        sample_game.update_projectiles(time_passed)
        self.assertEqual(sample_projectile.position.x, 0)

    def test_update_walls(self):
        sample_game = game.game = game.Game("tank", "berserker")
        sample_wall = wall.Wall(point.Point(10, 10), False, 100, 100)
        sample_wall.position.x = -50
        sample_game.walls = [sample_wall]
        time_passed = 20
        sample_game.update_walls(time_passed)
        self.assertEqual(len(sample_game.walls), 0)

if __name__ == '__main__':
    unittest.main()