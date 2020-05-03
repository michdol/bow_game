import pygame
from pygame.locals import *

from aim_line import AimLine
from arrow import Arrow
from character import Character
from constants import (
  FLOOR_Y,
  CHARACTER_WIDTH,
  CHARACTER_HEIGHT,
  SCREEN_WIDTH,
  SCREEN_HEIGHT
)
from colors import (
  BLACK,
  BLUE,
  GREEN,
  RED,
)
from enemy import Enemy


class App(object):
  def __init__(self):
    self._running = True
    self.clock = pygame.time.Clock()
    self.size = self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
    self.all_sprites = pygame.sprite.Group()
    self.character = None
    self.aim_line = None

  def on_init(self):
    pygame.init()
    self.screen = pygame.display.set_mode(self.size)
    self._running = True
    self.character = Character(RED, CHARACTER_WIDTH, CHARACTER_HEIGHT, self.screen)
    self.aim_line = AimLine(RED, CHARACTER_WIDTH, CHARACTER_HEIGHT, self.screen, self.character)
    self.arrows = []
    self.character.rect.x = 100
    self.character.draw_character_on_the_floor()
    self.all_sprites.add(self.character)
    self.click_position = None
    self.current_arrow = None
    self.arrows = []
    self.enemies = []
    self.enemy_create_counter = 0

  def on_event(self, event):
    mouse = pygame.mouse.get_pressed()
    if event.type == pygame.QUIT:
      self._running = False
    elif event.type == pygame.KEYDOWN:
      if event.key == K_ESCAPE:
        self._running = False
      elif event.key == K_SPACE:
        self.character.jump()
    elif event.type == pygame.MOUSEBUTTONDOWN:
      if mouse[0]:
        self.click_position = event.pos
        self.all_sprites.add(self.create_arrow(self.click_position))
    elif event.type == pygame.MOUSEBUTTONUP:
      if not mouse[0]:
        self.current_arrow.release(pygame.mouse.get_pos())
        self.click_position = None
        self.current_arrow = None

  def on_loop(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
      self.character.move_left()
    if keys[pygame.K_d]:
      self.character.move_right()
    if self.character.is_jumping:
      self.character.perform_jump()
    for arrow in self.arrows:
      arrow.set_center()
      arrow.update()
    self.arrows = [arrow for arrow in self.arrows if not arrow.stopped]
    self.create_enemy()
    for enemy in self.enemies:
      enemy.update()
    # self.enemies = [enemy for enemy in self.enemies if not enemy.delete]

  def on_render(self):
    self.screen.fill(GREEN)
    # Draw floor
    pygame.draw.rect(self.screen, BLACK, [0, FLOOR_Y, self.width, 1])
    self.all_sprites.draw(self.screen)
    if self.click_position:
      self.aim_line.draw(self.click_position)
    pygame.display.flip()

  def on_cleanup(self):
    pygame.quit()

  def on_execute(self):
    if self.on_init() is False:
      self._running = False

    while self._running:
      for event in pygame.event.get():
        self.on_event(event)
      self.on_loop()
      self.on_render()
      self.clock.tick(60)
    self.on_cleanup()

  def create_arrow(self, click_position):
    arrow = Arrow(BLUE, self.screen, self.character, click_position)
    self.current_arrow = arrow
    self.arrows.append(arrow)
    return arrow

  def create_enemy(self):
    self.enemy_create_counter += 1
    if self.enemy_create_counter == 120:
      enemy = Enemy(BLUE, self.screen, self.arrows, self.all_sprites)
      self.enemies.append(enemy)
      self.enemy_create_counter = 0
      self.all_sprites.add(enemy)


if __name__ == "__main__":
  theApp = App()
  theApp.on_execute()

# https://stackoverflow.com/questions/44465783/how-to-make-arrow-shoot-in-direction-of-mouse

# https://www.raywenderlich.com/2795-beginning-game-programming-for-teens-with-python#toc-anchor-008
