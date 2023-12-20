import pygame

class Game:
  def __init__(self):
    pygame.display.set_caption("Testing testing")
    self.is_running = True

  def handle_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.is_running = False

  def update(self):
    pass

  def render(self):
    pass
