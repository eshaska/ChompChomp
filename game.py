import pygame
import random

class Game:
  def __init__(self):
    pygame.display.set_caption("Your Game Title")
    self.width, self.height = 800, 600
    self.screen = pygame.display.set_mode((self.width, self.height))
    self.clock = pygame.time.Clock()
    self.is_running = True
    #self.in_game = False
    self.game_state = "intro"

    self.player_rect = pygame.Rect(100, 100, 50, 50)
    self.player_color = (255, 255, 255)
    self.player_health = 100

    self.lvl_1_monster_rect = pygame.Rect(400,500,50,50)
    self.lvl_1_monster_color = (255, 0, 0)
    self.monster_speed = 3  # Adjust the speed as needed
    self.monster_path = [(100, 400), (300, 400), (500, 400), (700, 400)]  # Example path

    self.gems = []
    self.generate_gems_positions()

    self.collided = False
    self.collided_timer = 0
    self.current_path_index = 0


  def generate_gems_positions(self):
    self.gems = [(random.randint(50, self.width - 50), random.randint(50, self.height - 50)) for _ in range(10)]


  def render_gems(self):
    gem_color = (255, 255, 0)  # Yellow color for gems
    for gem_position in self.gems:
      pygame.draw.circle(self.screen, gem_color, gem_position, 10)  # Assuming gems as circles


  def handle_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.is_running = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if self.game_state == "intro":
          click_rect_play = pygame.Rect(200, 300, 400, 100)
          click_rect_instructions = pygame.Rect(100, 300, 200, 50)
          if click_rect_play.collidepoint(event.pos):
            self.game_state = "playing"
          elif click_rect_instructions.collidepoint(event.pos):
            self.game_state = "instructions"

###########################
      """  elif self.game_state == "playing":
          # Assuming your winning condition
          if event.button == 1 and self.check_winning_condition(event.pos):
            self.game_state = "winning"
          elif self.game_state == "winning":
              # Handle click on the home button to transition back to the intro state
            if event.button == 1 and 100 <= event.pos[0] <= 200 and 100 <= event.pos[1] <= 150:
              self.game_state = "intro"
      """

  def render_health_bar(self):
    health_bar_width = (self.player_health / 100) * 200  # Adjust the multiplier and width as needed

    # Draw the health bar
    pygame.draw.rect(self.screen, (255, 0, 0), (50, 20, 200, 20))  # Red background
    pygame.draw.rect(self.screen, (0, 255, 0), (50, 20, health_bar_width, 20))  # Green foreground


  def update(self):
    keys = pygame.key.get_pressed()
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


    if not self.collided:
      if self.check_collision(self.player_rect, self.lvl_1_monster_rect):
        self.player_health -= 10  # Adjust the decrement as needed
        self.collided = True  # Set the collision flag
        if self.player_health <= 0:
          self.game_state = "losing"
    else:
      self.collided_timer += 1
      if self.collided_timer > 60:  # Adjust the value based on your needs
        self.collided = False
        self.collided_timer = 0
    # Check if the monster reached its target point
    distance_threshold = 5
    if (
        abs(self.lvl_1_monster_rect.x - target_x) <= distance_threshold
        and abs(self.lvl_1_monster_rect.y - target_y) <= distance_threshold
    ):
      self.current_path_index = (self.current_path_index + 1) % len(self.monster_path)

    if len(self.gems)>0:
      self.check_collision_gems()
    else:
      self.game_state = "winning"


  def check_collision(self, rect1, rect2):
    return rect1.colliderect(rect2)


  def check_collision_gems(self):
    for gem_position in self.gems:
      gem_rect = pygame.Rect(gem_position[0] - 10, gem_position[1] - 10, 20, 20)  # Assuming gem size is 20x20
      if self.check_collision(self.player_rect, gem_rect):
        self.gems.remove(gem_position)


  def render_instructions(self):
    self.screen.fill((10,182,193))
    instructions_font = pygame.font.Font(None, 64)
    instructions_text = instructions_font.render("How to Play: XXXXXX XXXXX", True, (255, 255, 255))
    instructions_rect = instructions_text.get_rect(center=(self.width // 2, self.height // 2))
    self.screen.blit(instructions_text, instructions_rect)
    self.render_home_button()
    pygame.display.flip()


  def render_intro_scene(self):
    self.screen.fill((255,182,193))
    self.game_state = "intro"
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

    instructions_box_rect = pygame.Rect(100, 300, 200, 50)
    pygame.draw.rect(self.screen, (255, 255, 255), instructions_box_rect)

    # Render and draw the text
    font = pygame.font.Font(None, 32)
    instructions_surface = font.render("How to Play", True, (0, 0, 0))

    # Define instructions_rect before using it
    instructions_rect = instructions_surface.get_rect(topleft=(instructions_box_rect.left + 10, instructions_box_rect.top + 10))

    self.screen.blit(instructions_surface, instructions_rect)

    #self.handle_events()
    pygame.display.flip()


  def render_game_scene(self):
    self.screen.fill((0,0,0))
    self.game_state = "playing"
    pygame.draw.rect(self.screen, self.player_color, self.player_rect)
    pygame.draw.rect(self.screen, self.lvl_1_monster_color, self.lvl_1_monster_rect)
    self.render_health_bar()
    self.render_gems()
    pygame.display.flip()

  
  def render_home_button(self):
    home_button_rect = pygame.Rect(300, 400, 200, 50)
    home_button_color = (0, 255, 0)
    pygame.draw.rect(self.screen, home_button_color, home_button_rect)

    home_button_font = pygame.font.Font(None, 36)
    home_button_text = home_button_font.render("Home", True, (0, 0, 0))
    home_button_text_rect = home_button_text.get_rect(center=home_button_rect.center)
    self.screen.blit(home_button_text, home_button_text_rect)
    #self.game_state = "intro"

    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.is_running = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if home_button_rect.collidepoint(event.pos):
          self.player_health = 100
          self.gems = []
          self.generate_gems_positions()
          self.game_state = "intro"
         # self.render_intro_scene()


    #event = pygame.event.poll()
    #if event.type == pygame.MOUSEBUTTONDOWN and home_button_rect.collidepoint(event.pos):
      #self.game_state = "intro"
     # elf.render_intro_scene()

    pygame.display.flip()


  def render_losing_scene(self):
    self.screen.fill((0,0,0))
    title_font = pygame.font.Font(None, 64)
    losing_text = title_font.render("You Lost!", True, (255,255,255))
    text_rect = losing_text.get_rect(center=(self.width // 2, self.height // 2))
    self.screen.blit(losing_text, text_rect)
    self.render_home_button()
    pygame.display.flip()


  def render_winning_scene(self):
    self.screen.fill((0,0,0))
    title_font = pygame.font.Font(None, 64)
    winning_text = title_font.render("You Won!", True, (255,255,255))
    text_rect = winning_text.get_rect(center=(self.width // 2, self.height // 2))
    self.screen.blit(winning_text, text_rect)
    self.render_home_button()
    pygame.display.flip()


  def run(self):
    while self.is_running:
     # print("Current game state:", self.game_state)
      self.handle_events()
      self.update()
      if self.game_state == "intro":
        self.render_intro_scene()
        self.player_health = 100
      elif self.game_state == "playing":
        self.render_game_scene()
      elif self.game_state == "losing":
        self.render_losing_scene()
       # self.render_home_button()
        #pygame.display.flip()
        #pygame.time.delay(2000)
        #self.game_state = "intro"
      elif self.game_state == "winning":
        self.render_winning_scene()
       # self.render_home_button()
        #pygame.display.flip()
       # pygame.time.delay(2000)
        #self.game_state = "intro"
      elif self.game_state == "instructions":
        self.render_instructions()
      
      pygame.display.flip()
      self.clock.tick(60)
