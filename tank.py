import character
import projectile
import point

class Tank(character.Character):

    SIZE = point.Point(90, 90)
    SPEED = 0.3
    RELOAD_TIME = 300
    PROJECTILE_TYPE = projectile.Projectile(point.Point(50, 50),
                                                 point.Point(10, 10),
                                                 1, 1, point.Point(0, 0))
    HEALTH = 350
    DAMAGE = 1
    ATTRIBUTES = [SIZE, SPEED, RELOAD_TIME, PROJECTILE_TYPE, HEALTH, DAMAGE]

    MISSILE_DAMAGE = 15
    MISSILE_HEALTH_COST = 15
    MISSLE_COOLDOWN = 600

    def __init__(self, position):
        character.Character.__init__(self, position, *Tank.ATTRIBUTES)
        self.aggressive_mode = False
        self.missile_cooldown = 0

    def use_skill(self):
        if self.aggressive_mode == False and self.missile_cooldown <= 0:
            self.damage = Tank.MISSILE_DAMAGE
            self.health -= Tank.MISSILE_HEALTH_COST
            self.projectile_type.size.x *= 3.5
            self.projectile_type.size.y *= 3.5
            self.aggressive_mode = True
            self.missile_cooldown = Tank.MISSLE_COOLDOWN 

    def update(self, time_passed):
        character.Character.update(self, time_passed)
        self.missile_cooldown -= time_passed

    def shoot(self):
        shot = character.Character.shoot(self)
        if self.aggressive_mode == True:
            self.damage = Tank.DAMAGE
            self.aggressive_mode = False
            self.projectile_type.size.x /= 3.5
            self.projectile_type.size.y /= 3.5
        return shot
