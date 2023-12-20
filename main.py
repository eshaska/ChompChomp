import pygame
from game import Game
pygame.init()

game = Game()

while game.is_running():
  game.handle_events()
  game.update()
  game.render()

pygame.quit()
