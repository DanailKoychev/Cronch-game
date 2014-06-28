from game import *
import time

from gui import render_via_pygame as render
from wall import *
from bot import *

FPS = 120

pygame.init()
game = Game(0)
bot = Bot(game.player_2, game)
clock = pygame.time.Clock()

while True:
    time_passed = clock.tick(FPS)
    game.update(controls.get_keyboard_input_player_1(), bot.get_input(), time_passed)
    render(game)

    if not game.player_1.alive:
        render(game)
        break
    if not game.player_2.alive:
        render(game)
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
time.sleep(2)