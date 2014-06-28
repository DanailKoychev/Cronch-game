import unittest
import berserker
import point

class BerserkerTest(unittest.TestCase):
    def test_update(self):
        position = point.Point(50, 70)
        player = berserker.Berserker(point)
        initial_damage = player.damage
        initial_speed = player.speed
        initial_reload_time = player.reload_time_millisec
        player.health /= 2
        time_passed = 20
        player.update(time_passed)
        self.assertEqual(player.damage, berserker.Berserker.DAMAGE * \
                         berserker.Berserker.DAMAGE_AMPLIFIER / 2)
        self.assertEqual(player.speed, berserker.Berserker.SPEED * \
                         berserker.Berserker.SPEED_AMPLIFIER / 2)
        self.assertEqual(player.reload_time_millisec, 
                         berserker.Berserker.RELOAD_TIME +
                         berserker.Berserker.RELOAD_TIME * \
                         berserker.Berserker.RELOAD_TIME_AMPLIFIER / 2)

if __name__ == '__main__':
    unittest.main()