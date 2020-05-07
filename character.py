from math import sin, radians
from pygame import draw, mouse, image
from pygame.sprite import Sprite

from constants import (
  CHARACTER_HEIGHT,
  CHARACTER_SPRITE_WIDTH,
  CHARACTER_SPRITE_HEIGHT,
  CHARACTER_SPEED,
  CHARACTER_JUMP_FRAMES,
  FLOOR_Y,
)


class Character(Sprite):
  def __init__(self, color, width, height, screen):
    Sprite.__init__(self)
    # Pass in the color of the car, and its x and y position, width and height.
    # Set the background color and set it to be transparent
    self.color = color
    """
    # Old character drawing
    self.image = Surface([width, height])
    self.image.fill(color)
    draw.rect(self.image, color, [0, 0, CHARACTER_SPRITE_WIDTH, CHARACTER_SPRITE_HEIGHT])
    """

    self.is_jumping = False
    self.jumpCnt = CHARACTER_JUMP_FRAMES
    self.screen = screen
    self.t = 0
    self.run_t = 0
    self.is_running = False
    self.is_facing_right = True

    # Instead we could load a proper pciture of a car.. .
    self.load_idle_image()
    # Fetch the rectangle object that has the dimensions of the image.
    self.rect = self.image.get_rect()

  def get_center(self):
    return self.rect.center

  def collidepoint(self, position):
    return self.rect.collidepoint(position) == 1

  def move_left(self):
    self.is_running = True
    self.rect.move_ip(-CHARACTER_SPEED, 0)

  def move_right(self):
    self.is_running = True
    self.rect.move_ip(CHARACTER_SPEED, 0)

  def stop(self):
    self.is_running = False
    self.run_t = 0
    self.load_idle_image()

  def jump(self):
    if not self.is_jumping:
      self.is_jumping = True

  def perform_jump(self):
    if self.is_jumping:
      t = self.t
      g = 0.980
      speed = 5
      vy = -sin(radians(75)) * speed + 0.5 * g * t * t
      self.rect.y += vy
      self.t += 0.1
      if self.rect.y >= FLOOR_Y - 0.5 * CHARACTER_SPRITE_HEIGHT:
        self.is_jumping = False
        self.draw_character_on_the_floor()
        self.t = 0

  def draw_character_on_the_floor(self):
    self.rect.y = FLOOR_Y - CHARACTER_SPRITE_HEIGHT

  def load_idle_image(self):
    direction = self.get_facing_direction_string()
    sprite_name = self.get_tile_name(direction, 1)
    self.image = image.load(sprite_name).convert_alpha()

  def run_animation(self):
    if not self.is_running:
      return
    # 60 fps / 15 tiles = 4 frames per tile
    quotient = self.run_t // 4
    direction = self.get_facing_direction_string()
    name = self.get_tile_name(direction, quotient)
    self.image = image.load(name).convert_alpha()
    if self.run_t > 15:
      self.run_t = 0
    self.run_t += 1

  def get_tile_name(self, direction: str, index: int) -> str:
    return "sprites/run_{direction}/tile0{index:02}.png".format(
      direction=direction,
      index=index
    )

  def get_facing_direction_string(self) -> str:
    return "right" if self.is_facing_right else "left"

  def set_facing_direction(self):
    mouse_x, _ = mouse.get_pos()
    self.is_facing_right = self.rect.x > mouse_x
