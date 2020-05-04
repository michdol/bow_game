from pygame import Surface, draw
from pygame.sprite import Sprite

from constants import (
  SCREEN_WIDTH,
  CHARACTER_WIDTH,
  CHARACTER_HEIGHT,
  FLOOR_Y,
)


class Enemy(Sprite):
  def __init__(self, color, screen, app, sprites_group):
    Sprite.__init__(self)
    self.color = color
    self.screen = screen
    self.app = app
    self.delete = False
    self.sprites_group = sprites_group

    self.image = Surface([CHARACTER_WIDTH, CHARACTER_HEIGHT])
    self.image.fill(color)
    draw.rect(self.image, color, [0, 0, CHARACTER_WIDTH, CHARACTER_HEIGHT])
    self.rect = self.image.get_rect()
    self.rect.x = SCREEN_WIDTH + CHARACTER_WIDTH
    self.rect.y = FLOOR_Y - CHARACTER_HEIGHT

  def update(self):
    if self.rect.x < 0:
      self.delete = True
    self.rect.x -= 1

    for arrow in self.app.arrows:
      self.delete = self.rect.colliderect(arrow.rect)
      if self.delete:
        arrow.hit()
        self.rect.x = -CHARACTER_WIDTH
        self.sprites_group.remove(self)
