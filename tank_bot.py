import bot
import controls

class TankBot(bot.Bot):
    def get_input(self):
        instructions = bot.Bot.get_input(self)
        if not self.defensive:
            if self.character.health > 1.5 * self.enemy.health:
                instructions.append(controls.Controls.USE_SKILL)
        return instructions