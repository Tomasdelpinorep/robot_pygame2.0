import pygame

from game import Game
import sys

g = Game()
# g.intro_screen()
g.new()

while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
