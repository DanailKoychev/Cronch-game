import unittest
import bot
import projectile
import point
import berserker
import game
import controls

class BotTest(unittest.TestCase):
    def test_get_movement_range(self):
        sample_game = game.Game("tank", "tank")
        sample_character = berserker.Berserker(point.Point(20, 20))
        sample_bot = bot.Bot(sample_character, sample_game)
        movement_range = sample_bot.get_movement_range(sample_character, 1)

        self.assertEqual(movement_range, (19.6, 20.4))

    def test_snipe(self):
        sample_game = game.Game("tank", "tank")
        sample_character = berserker.Berserker(point.Point(20, 20))
        sample_bot = bot.Bot(sample_character, sample_game)
        sample_bot.enemy.position = point.Point(100, 100)
        sample_bot.snipe()
        self.assertEqual(sample_bot.character.aim.x, 100)     

    def test_manage_shooting(self):
        sample_game = game.Game("tank", "tank")
        sample_character = berserker.Berserker(point.Point(20, 20))
        sample_bot = bot.Bot(sample_character, sample_game)
        sample_bot.character.disarmed = True
        self.assertIsNone(sample_bot.manage_shooting())

    def test_move_towards(self):
        sample_game = game.Game("tank", "tank")
        sample_character = berserker.Berserker(point.Point(20, 20))
        sample_bot = bot.Bot(sample_character, sample_game)
        instructions = sample_bot.move_towards(40)
        self.assertEqual(controls.Controls.MOVE_RIGHT, instructions)     

    def test_move_away(self):
        sample_game = game.Game("tank", "tank")
        sample_character = berserker.Berserker(point.Point(20, 20))
        sample_bot = bot.Bot(sample_character, sample_game)
        instructions = sample_bot.move_away(40)
        self.assertEqual(controls.Controls.MOVE_LEFT, instructions)

    def update(self, time_passed):
        sample_game = game.Game("tank", "tank")
        sample_character = berserker.Berserker(point.Point(20, 20))
        sample_bot = bot.Bot(sample_character, sample_game)
        sample_bot.time_until_behavior_change = 300
        sample_bot.update(243)
        self.assertEqual(sample_bot.time_until_behavior_change, 57)
        sample_bot.update(500)
        self.assertTrue(sample_bot.time_until_behavior_change >= 0)

if __name__ == '__main__':
    unittest.main()