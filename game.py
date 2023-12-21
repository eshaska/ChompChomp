import pygame

#make how to play page
#make it so game ends if monster touches
#make designs of characters better-unlockable?
#make home button
#make food for player
#make health bar
#make other monsters with different powers and paths
#fix aesthetics
#make other levels?
#fix comments and put into github

class Game:
  def __init__(self):
    pygame.display.set_caption("Your Game Title")
    self.width, self.height = 800, 600
    self.screen = pygame.display.set_mode((self.width, self.height))
    self.clock = pygame.time.Clock()
    self.is_running = True
    self.in_game = False

    self.player_rect = pygame.Rect(100, 100, 50, 50)
    self.player_color = (255, 255, 255)
    self.player_health = 100

    self.lvl_1_monster_rect = pygame.Rect(400,500,50,50)
    self.lvl_1_monster_color = (255, 0, 0)
    self.monster_speed = 3  # Adjust the speed as needed
    self.monster_path = [(100, 400), (300, 400), (500, 400), (700, 400)]  # Example path

    self.current_path_index = 0


  def handle_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.is_running = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if not self.in_game:
          click_rect = pygame.Rect(200, 300, 400, 100)
          if click_rect.collidepoint(event.pos):
            self.in_game = True


  def render_health_bar(self):
    health_bar_width = (self.player_health / 100) * 200  # Adjust the multiplier and width as needed

    # Draw the health bar
    pygame.draw.rect(self.screen, (255, 0, 0), (50, 20, 200, 20))  # Red background
    pygame.draw.rect(self.screen, (0, 255, 0), (50, 20, health_bar_width, 20))  # Green foreground


  def update(self):
    keys = pygame.key.get_pressed()
        # Adjust character's position based on arrow key presses
    if keys[pygame.K_LEFT]:
      self.player_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        self.player_rect.x += 5
    if keys[pygame.K_UP]:
        self.player_rect.y -= 5
    if keys[pygame.K_DOWN]:
        self.player_rect.y += 5

    # Move the monster automatically along the predefined path
    target_x, target_y = self.monster_path[self.current_path_index]

    # Move towards the target point
    if self.lvl_1_monster_rect.x < target_x:
      self.lvl_1_monster_rect.x += self.monster_speed
    elif self.lvl_1_monster_rect.x > target_x:
      self.lvl_1_monster_rect.x -= self.monster_speed

    if self.lvl_1_monster_rect.y < target_y:
      self.lvl_1_monster_rect.y += self.monster_speed
    elif self.lvl_1_monster_rect.y > target_y:
      self.lvl_1_monster_rect.y -= self.monster_speed

      # Check for collision between player and monster
    if self.check_collision(self.player_rect, self.lvl_1_monster_rect):
      self.player_health -= 10  # Adjust the decrement as needed
      if self.player_health <= 0:
        self.render_losing_scene()

    # Check if the monster reached its target point
    distance_threshold = 5
    if (
        abs(self.lvl_1_monster_rect.x - target_x) <= distance_threshold
        and abs(self.lvl_1_monster_rect.y - target_y) <= distance_threshold
    ):
        self.current_path_index = (self.current_path_index + 1) % len(self.monster_path)


  def check_collision(self, rect1, rect2):
    return rect1.colliderect(rect2)


  def render_intro_scene(self):
    self.screen.fill((255,182,193))
    # Draw a rectangle for the title
    title_rect = pygame.Rect(50, 50, 700, 100)
    title_color = (0, 0, 255)  # Blue color for the title
    pygame.draw.rect(self.screen, title_color, title_rect)

    # Draw text for the title
    title_font = pygame.font.Font(None, 64)
    title_text = title_font.render("Game Title XX", True, (255, 255, 255))
    title_text_rect = title_text.get_rect(center=title_rect.center)
    self.screen.blit(title_text, title_text_rect)

    # Draw a rectangle for "Click to Play"
    click_rect = pygame.Rect(200, 300, 400, 100)
    click_color = (0, 255, 0)  # Green color for "Click to Play"
    pygame.draw.rect(self.screen, click_color, click_rect)

    # Draw text for "Click to Play"
    click_font = pygame.font.Font(None, 36)
    click_text = click_font.render("Click to Play", True, (0, 0, 0))
    click_text_rect = click_text.get_rect(center=click_rect.center)
    self.screen.blit(click_text, click_text_rect)
    pygame.display.flip()


  def render_game_scene(self):
    self.screen.fill((0,0,0))
    pygame.draw.rect(self.screen, self.player_color, self.player_rect)
    pygame.draw.rect(self.screen, self.lvl_1_monster_color, self.lvl_1_monster_rect)
    self.render_health_bar()
    pygame.display.flip()
  

  def render_losing_scene(self):
    self.screen.fill((0,0,0))
    title_font = pygame.font.Font(None, 64)
    losing_text = title_font.render("You Lost!", True, (255,255,255))
    text_rect = losing_text.get_rect(center=(self.width // 2, self.height // 2))
    self.screen.blit(losing_text, text_rect)
    pygame.display.flip()


  def run(self):
    while self.is_running:
      self.handle_events()
      self.update()
      if self.in_game:
        self.render_game_scene()
      else:
        self.render_intro_scene()
     # if self.check_collision(self.player_rect, self.lvl_1_monster_rect):

      #  self.render_losing_scene()
      self.clock.tick(60)
