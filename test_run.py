from game import *
import time

from gui import render_via_pygame as render
from wall import *
from bot import * 

game = Game(0)
bot = Bot(game.player_2, game)

while True:
    game.update(controls.get_keyboard_input(), bot.get_input())
    render(game)

    if not game.player_1.alive:
        render(game)
        break
    if not game.player_2.alive:
        render(game)
        break

time.sleep(2)
