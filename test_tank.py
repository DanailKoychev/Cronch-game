import unittest
import tank
import point

class TankTest(unittest.TestCase):
    def test_init(self):
        position = point.Point(20, 20)
        player = tank.Tank(position)
        self.assertFalse(player.aggressive_mode)
        self.assertEqual(player.missile_cooldown, 0)

    def test_use_skill(self):
        position = point.Point(20, 20)
        player = tank.Tank(position)
        player.aggressive_mode = False
        player.use_skill()
        self.assertTrue(player.aggressive_mode)
        self.assertEqual(player.damage, tank.Tank.MISSILE_DAMAGE)
        self.assertEqual(player.health, 335)    #initial health is 350

        player = tank.Tank(position)
        player.missile_cooldown = 15
        player.use_skill()
        self.assertFalse(player.aggressive_mode)
        self.assertEqual(player.damage, tank.Tank.DAMAGE)

    def test_update(self):
        player = tank.Tank(point.Point(20, 20))
        player.missile_cooldown = 120
        player.update(40)
        self.assertEqual(player.missile_cooldown, 80)

    def test_shoot(self):
        player = tank.Tank(point.Point(20, 20))
        player.use_skill()
        shot = player.shoot()
        self.assertEqual(shot.damage, tank.Tank.MISSILE_DAMAGE)
        self.assertEqual(shot.size.x, tank.Tank.PROJECTILE_TYPE.size.x * 3.5)
        self.assertEqual(shot.size.y, tank.Tank.PROJECTILE_TYPE.size.y * 3.5)

if __name__ == '__main__':
    unittest.main()