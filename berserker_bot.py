import bot
import controls
import berserker

class Berserker_bot(bot.Bot):
    def update(self, time_passed):
        bot.Bot.update(self, time_passed)
        if self.character.health > (2 / 3) * berserker.Berserker.HEALTH:
            self.defensive = False
        if self.character.health < (1 / 5) * berserker.Berserker.HEALTH:
            self.defensive = True;
