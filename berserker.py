import character
import projectile
import point

class Berserker(character.Character):

    SIZE = point.Point(50, 50)
    SPEED = 0.4
    RELOAD_TIME = 150
    HEALTH = 120
    DAMAGE = 4
    PROJECTILE_TYPE = projectile.Projectile(point.Point(0, 0),
                                            point.Point(10, 10),
                                            1, 3, point.Point(0, 0))

    ATTRIBUTES = [SIZE, SPEED, RELOAD_TIME, PROJECTILE_TYPE,
                            HEALTH, DAMAGE]

    SPEED_AMPLIFIER = 3
    RELOAD_TIME_AMPLIFIER = 3
    DAMAGE_AMPLIFIER = 2

    def __init__(self, position):
        character.Character.__init__(self, position, *Berserker.ATTRIBUTES)

    def update(self, time_passed):
        character.Character.update(self, time_passed)
        current_health_percent = self.health / Berserker.HEALTH
        missing_health_percent = 1 - current_health_percent
        self.speed = Berserker.SPEED + Berserker.SPEED * \
                     missing_health_percent * Berserker.SPEED_AMPLIFIER
        self.reload_time_millisec = Berserker.RELOAD_TIME + \
                                    Berserker.RELOAD_TIME * \
                                    current_health_percent * \
                                    Berserker.RELOAD_TIME_AMPLIFIER
        self.damage = Berserker.DAMAGE + Berserker.DAMAGE * \
                      missing_health_percent * \
                      Berserker.DAMAGE_AMPLIFIER

    def use_skill(self):
        pass

