import unittest
import character
import point
import projectile

class CharacterTest(unittest.TestCase):
    def test_init_character(self):
        projectile_type = projectile.Projectile(point.Point(0, 0),
                                point.Point(5,5), 5, 0, point.Point(0, 0)),
        attributes = [point.Point(10, 20), point.Point(30, 40), 0.5, 300,
                      projectile_type, 100, 10]
        sample_character = character.Character(*attributes)
        self.assertEqual(sample_character.x, 10)
        self.assertEqual(sample_character.y, 20)
        self.assertEqual(sample_character.size.x, 30)
        self.assertEqual(sample_character.size.y, 40)
        self.assertEqual(sample_character.speed, 0.5)
        self.assertEqual(sample_character.reload_time_millisec, 300)
        self.assertIs(sample_character.projectile_type, projectile_type)
        self.assertEqual(sample_character.health, 100)
        self.assertEqual(sample_character.damage, 10)
        self.assertTrue(sample_character.ready_to_shoot)
        self.assertTrue(sample_character.alive)
        self.assertFalse(sample_character.vampire)
        self.assertEqual(len(sample_character.own_projectiles), 0)

    def test_move(self):
        attributes = [point.Point(10, 20), point.Point(30, 40), 0.5, 300,
                      None, 100, 10]
        sample_character = character.Character(*attributes)
        sample_character.move_left(200)
        self.assertEqual(sample_character.x, -90)
        sample_character.move_right(300)
        self.assertEqual(sample_character.x, 60)

    def test_shoot(self):
        projectile_type = projectile.Projectile(point.Point(0, 0),
                            point.Point(5, 5), 0.5, 0, point.Point(0, 0))
        attributes = [point.Point(10, 20), point.Point(30, 40), 0.5, 300,
                      projectile_type, 100, 10]
        sample_character = character.Character(*attributes)
        shot = sample_character.shoot()
        expected_projectile = projectile.Projectile(point.Point(10, 20),
                                                    point.Point(5, 5),
                                                    0.5, 10, point.Point(0, 0),
                                                    sample_character)
        self.assertEqual(expected_projectile.speed,
                         shot.speed)
        self.assertEqual(shot, expected_projectile)       

    def test_start_reloading(self):
        attributes = [point.Point(10, 20), point.Point(30, 40), 0.5, 300,
                      None, 100, 10]
        sample_character = character.Character(*attributes)
        sample_character.start_reloading()
        self.assertFalse(sample_character.ready_to_shoot)
        self.assertEqual(sample_character.reload_time_left,
                         sample_character.reload_time_millisec)

    def test_move_aim(self):
        attributes = [point.Point(10, 20), point.Point(30, 40), 0.5, 300,
                      None, 100, 10]
        sample_character = character.Character(*attributes)
        sample_character.move_aim_right(200)
        self.assertEqual(sample_character.aim.x, 140)
        sample_character.move_aim_left(300)
        self.assertEqual(sample_character.aim.x, - 70)
        sample_character.move_aim_left(0)
        self.assertEqual(sample_character.aim.x, - 70)

    def test_update(self):
        attributes = [point.Point(10, 20), point.Point(30, 40), 0.5, 300,
                      None, 100, 10]
        sample_character = character.Character(*attributes)
        sample_character.disarmed = True
        sample_character.disarm_time_left = 200
        sample_character.snared = True
        sample_character.snare_time_left = 5
        sample_character.vampire = False
        sample_character.update(100)
        self.assertTrue(sample_character.disarmed)
        self.assertEqual(sample_character.disarm_time_left, 100)
        self.assertFalse(sample_character.snared)
        self.assertFalse(sample_character.vampire)
        sample_character.health = - 10
        sample_character.update(0)
        self.assertFalse(sample_character.alive)

    def test_get_hit(self):
        attributes = [point.Point(10, 20), point.Point(30, 40), 0.5, 300,
                      None, 100, 10]
        sample_character = character.Character(*attributes)
        sample_projectile = projectile.Projectile(point.Point(10, 20),
                                point.Point(5,5), 5, 10, point.Point(0, 0))
        sample_character.get_hit(sample_projectile)
        self.assertEqual(sample_character.health, 90)

if __name__ == '__main__':
    unittest.main()