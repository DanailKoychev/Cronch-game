import character
import projectile
import point

TANK_SIZE = point.Point(80, 80)
TANK_SPEED = 0.3
TANK_RELOAD_TIME = 300
TANK_PROJECTILE_TYPE = projectile.Projectile(point.Point(50, 50),
                                             point.Point(10, 10),
                                             1, 1, point.Point(0, 0))
TANK_HEALTH = 350
TANK_DAMAGE = 1

MISSLE_DAMAGE = 15
MISSLE_HEALTH_COST = 15

class Tank(character.Character):

    def __init__(self, position):
        character.Character.__init__(self, position, TANK_SIZE,
            TANK_SPEED, TANK_RELOAD_TIME, TANK_PROJECTILE_TYPE,
            TANK_HEALTH, TANK_DAMAGE)
        self.aggressive_mode = False

    def use_skill(self):
        if self.aggressive_mode == False:
            self.damage = MISSLE_DAMAGE
            self.health -= MISSLE_HEALTH_COST
            self.projectile_type.size.x *= 3.5
            self.projectile_type.size.y *= 3.5
            self.aggressive_mode = True

    def shoot(self):
        shot = character.Character.shoot(self)
        if self.aggressive_mode == True:
            self.damage = TANK_DAMAGE
            self.aggressive_mode = False
            self.projectile_type.size.x /= 3.5
            self.projectile_type.size.y /= 3.5
        return shot
