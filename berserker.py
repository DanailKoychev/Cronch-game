import character
import projectile
import point

BERSERKER_SIZE = point.Point(60, 60)
BERSERKER_SPEED = 0.4
BERSERKER_RELOAD_TIME = 150
BERSERKER_PROJECTILE_TYPE = projectile.Projectile(point.Point(50, 50),
                                                  point.Point(10, 10),
                                                  1, 3, point.Point(0, 0))
BERSERKER_HEALTH = 150
BERSERKER_DAMAGE = 4

SPEED_AMPLIFIER = 3
RELOAD_TIME_AMPLIFIER = 3
DAMAGE_AMPLIFIER = 2

class Berserker(character.Character):

    def __init__(self, position):
        character.Character.__init__(self, position, BERSERKER_SIZE,
              BERSERKER_SPEED, BERSERKER_RELOAD_TIME, 
              BERSERKER_PROJECTILE_TYPE, BERSERKER_HEALTH,
              BERSERKER_DAMAGE)

    def update(self, time_passed):
        character.Character.update(self, time_passed)
        current_health_percent = self.health / BERSERKER_HEALTH
        missing_health_percent = 1 - current_health_percent
        self.speed = BERSERKER_SPEED * missing_health_percent * SPEED_AMPLIFIER
        self.reload_time_millisec = BERSERKER_RELOAD_TIME + \
                                    BERSERKER_RELOAD_TIME * \
                                    current_health_percent * \
                                    RELOAD_TIME_AMPLIFIER
        self.damage = BERSERKER_DAMAGE * missing_health_percent * \
                      DAMAGE_AMPLIFIER

    def use_skill(self):
        pass

