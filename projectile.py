import vec2d
import point

class Projectile():
    def __init__(self, position, size, speed, damage, aim, owner=None):
        self.position = position
        self.size = size
        self.speed = speed
        self.damage = damage
        self.aim = point.Point(aim.x, aim.y)
        self.owner = owner
        self.movement_vector = self.get_movement_vector(self.aim)

    def get_movement_vector(self, aim):
        if aim.x == self.position.x and aim.y == self.position.y:
            return vec2d.Vec2D(0, 0)
        movement_vector = vec2d.Vec2D(aim.x - self.position.x,
                                 aim.y - self.position.y)
        movement_vector.set_length(1)
        return movement_vector

    def update(self, time_passed):
        self.position += self.movement_vector * self.speed * time_passed

    def reflect_horizontally(self, x_position):
        self.position.x = x_position
        self.aim.x = 2 * x_position - self.aim.x
        self.movement_vector.x = -self.movement_vector.x

    def __eq__(self, other):
        return self.position == other.position and self.damage == other.damage\
            and self.movement_vector == other.movement_vector and \
            self.position == other.position and self.size == other.size \
            and self.speed == other.speed and self.owner == other.owner and \
            self.aim == other.aim

    @property
    def x(self):
        return self.position.x
    @x.setter
    def x(self, value):
        self.position = value

    @property
    def y(self):
        return self.position.y
    @y.setter
    def y(self, value):
        self.position.y = value
    
    
