import pygame
from game import Game
pygame.init()

game = Game()

print("outside the loop")
"""while game.is_running:
  print("inside the loop")
  game.handle_events()
  game.update()
  game.render()
"""
pygame.quit()
