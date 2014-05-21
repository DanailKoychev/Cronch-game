from game import *
from pygame.time import Clock
from gui import render_via_pygame as render

game = Game(0)
clock = Clock()

while True:
    time_passed = clock.tick(60)
    #game.get_all_players_input()
    game.update(time_passed)
    render(game)
