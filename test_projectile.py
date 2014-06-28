import unittest
import vec2d
import projectile
import point

class ProjectileTest(unittest.TestCase):
    def test_init_projectile(self):
        sample_projectile = projectile.Projectile(point.Point(10, 12),
                                                  point.Point(20, 21),
                                                  0.5, 10,
                                                  point.Point(10, 25))
        self.assertEqual(sample_projectile.position.x, 10)
        self.assertEqual(sample_projectile.position.y, 12)
        self.assertEqual(sample_projectile.size.x, 20)
        self.assertEqual(sample_projectile.size.y, 21)
        self.assertEqual(sample_projectile.speed, 0.5)
        self.assertEqual(sample_projectile.damage, 10)
        self.assertIs(sample_projectile.owner, None)
        self.assertEqual(sample_projectile.movement_vector, vec2d.Vec2D(0, 1))

    def test_get_movement_vector(self):
        sample_projectile = projectile.Projectile(point.Point(10, 12),
                                                  point.Point(20, 21),
                                                  0.5, 10,
                                                  point.Point(7, 8))
        aim = point.Point(11, 12)
        self.assertEqual(sample_projectile.get_movement_vector(aim),
                         vec2d.Vec2D(1, 0))
        aim = point.Point(10, -20)
        self.assertEqual(sample_projectile.get_movement_vector(aim),
                         vec2d.Vec2D(0, -1))
        aim = point.Point(10, 12)
        self.assertEqual(sample_projectile.get_movement_vector(aim),
                         vec2d.Vec2D(0, 0))

    def test_update(self):
        sample_projectile = projectile.Projectile(point.Point(10, 12),
                                                  point.Point(20, 21),
                                                  0.5, 10,
                                                  point.Point(17, 12))
        sample_projectile.update(200)
        self.assertEqual(sample_projectile.position, point.Point(110.0, 12.0))
        sample_projectile_2 = projectile.Projectile(point.Point(10, 12),
                                                  point.Point(20, 21),
                                                  0.5, 10,
                                                  point.Point(10, 12))
        self.assertEqual(sample_projectile_2.position, point.Point(10, 12))

    def test_reflect_horizontally(self):
        sample_projectile = projectile.Projectile(point.Point(10, 12),
                                                  point.Point(20, 21),
                                                  0.5, 10,
                                                  point.Point(17, 12))
        movement_vector_x = sample_projectile.movement_vector.x
        movement_vector_y = sample_projectile.movement_vector.y
        sample_projectile.reflect_horizontally(12)
        self.assertEqual(sample_projectile.movement_vector,
                         vec2d.Vec2D(- movement_vector_x, movement_vector_y))

    def test_equ(self):
        sample_projectile = projectile.Projectile(point.Point(10, 12),
                                                  point.Point(20, 21),
                                                  0.5, 10,
                                                  point.Point(17, 12))
        sample_projectile_2 = projectile.Projectile(point.Point(10, 12),
                                                  point.Point(20, 21),
                                                  0.5, 10,
                                                  point.Point(17, 12))
        sample_projectile_3 = projectile.Projectile(point.Point(999, 777),
                                                  point.Point(20, 21),
                                                  0.5, 10,
                                                  point.Point(17, 12))
        self.assertEqual(sample_projectile, sample_projectile_2)
        self.assertNotEqual(sample_projectile, sample_projectile_3)

if __name__ == '__main__':
    unittest.main()