import unittest
import wall
import point

class WallTests(unittest.TestCase):
    def test_init_wall(self):
        sample_wall = wall.Wall(point.Point(20, 10), True, 400, 600)
        self.assertEqual(sample_wall.size.x, 20)
        self.assertEqual(sample_wall.size.y, 10)
        self.assertIs(sample_wall.going_right, True)
        self.assertEqual(sample_wall.position.x, -10)
        self.assertEqual(sample_wall.position.y, 300)
        sample_wall_2 = wall.Wall(point.Point(20, 10), False, 400, 600)
        self.assertEqual(sample_wall_2.position.x, 410)

    def test_move(self):
        sample_wall = wall.Wall(point.Point(20, 10), False, 400, 600)
        sample_wall.move_left(3000)
        expected_position_x = 410 - wall.Wall.SPEED * 3000
        self.assertEqual(sample_wall.position.x, expected_position_x)
        sample_wall_2 = wall.Wall(point.Point(20, 10), False, 400, 600)
        sample_wall_2.move_right(4000)
        expected_position_2_x = 410 + wall.Wall.SPEED * 4000
        self.assertEqual(sample_wall_2.position.x, expected_position_2_x)

    def test_update(self):
        sample_wall = wall.Wall(point.Point(20, 10), False, 400, 600)
        sample_wall.update(4000)
        expected_position_x = 410 - wall.Wall.SPEED * 4000
        self.assertEqual(sample_wall.position.x, expected_position_x)

if __name__ == '__main__':
    unittest.main()