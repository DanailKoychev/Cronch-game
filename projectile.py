from pygame.sprite import Sprite, Group, Rect
from pygame.math import Vector2 as Vector

class Projectile(Sprite):
    def __init__(self, image, position, speed, damage):
        Sprite.__init__(self)
        self.rect = image.get_rect()
        self.position = position
        self.image = image
        self.speed = speed
        self.damage = damage

    @property
    def position(self):
        return self._position
    @position.setter
    def position(self, value):
        self.rect.x = value.x
        self.rect.y = value.y
        self._position = value

    def get_movement_vector(self, aim):
        movement_vector = Vector(aim.x - self.position.x,
                                 aim.y - self.position.y)
        movement_vector = movement_vector.normalize()
        return movement_vector

    def update(self, time_passed):
        #
        #self.movement_vector = self.get_movement_vector()
        self.position += self.movement_vector * self.speed * time_passed 

    def reflect_horizontally(self, x_position):
        self._position.x = x_position
        self.movement_vector.x = -self.movement_vector.x
#
    def reflect_vertically(self, field_height):
        self.movement_vector.y = -self.movement_vector.y

# FINISH 
# use instance of
    def hit(self, obstacle):
        if obstacle.__class__ is Character:
            character.health -= self.damage
            self.die()
        if obstacle.__class__ is Wall:
            if obstacle.power_up is not None:
                pass
                #apply
            # self.reflect_vertically(self,position.y)

# remove group from pygame sprite?
    def die(self):
        for group in self.groups():
            group.remove(self)


# verically only
    def is_in_screen(self, screen_height):
        if self.position.y + self.image.get_width() < 0 or \
           self.position.y > screen_height:
            return False
        return True

    def is_in_play_field(self, screen_height):
        if self.position.y < 3 or \
           self.position.y > screen_height - 3:
            return False
        return True



