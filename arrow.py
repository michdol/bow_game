from math import degrees, sqrt, sin, cos, atan, radians
from pygame import Surface, draw
from pygame.sprite import Sprite

from constants import ARROW_MAX_SPEED, FLOOR_Y
from game_types import Radian, Degree


class Arrow(Sprite):
  def __init__(self, color, screen, character, click_position):
    Sprite.__init__(self)
    self.color = color
    self.screen = screen
    self.character = character
    self.click_position = click_position

    width, height = 2, 2
    self.image = Surface([width, height])
    self.image.fill(color)
    draw.rect(self.image, color, [0, 0, width, height])
    self.rect = self.image.get_rect()
    self.released = False
    self.release_speed = None
    self.release_position = None
    self.angle: Degree = None
    self.t = 0
    self.is_moving_right = False
    self.stopped = False

  def set_center(self):
    if self.released:
      return
    x, y = self.character.get_center()
    self.rect.x = x
    self.rect.y = y

  def update(self):
    if self.rect.y >= FLOOR_Y:
      self.stopped = True
    if not self.released:
      return
    speed = self.release_speed
    t = self.t
    g = 0.980

    vx = cos(self.angle) * speed
    vy = -sin(self.angle) * speed + 0.5 * g * t * t
    # print("angle {} -sin(angle) {:0<25} 0.5 * g * t * t {:0<25}".format(self.angle, -sin(self.angle), 0.5*g*t*t))

    self.rect.x += vx
    self.rect.y += vy
    self.t += 0.1

  def release(self, release_position):
    if self.released:
      return
    self.released = True
    click_x, click_y = self.click_position
    self.release_position = release_x, release_y = release_position
    if release_x < click_x:
      self.is_moving_right = True
    adjacent, opposite = self.get_catheuses()
    angle: Degree = self.get_release_angle(adjacent, opposite)
    aiming_down = release_y < click_y
    self.angle = self.adjust_angle_to_aim_direction(angle, aiming_down, self.is_moving_right)
    length = self.get_line_length(adjacent, opposite)
    self.release_speed = self.get_release_speed(length)

  def get_catheuses(self):
    click_x, click_y = self.click_position
    release_x, release_y = self.release_position
    adjacent = abs(release_x - click_x)
    opposite = abs(release_y - click_y)
    return adjacent, opposite

  def get_release_angle(self, adjacent: float, opposite: float) -> Degree:
    if adjacent == 0:
      return 90
    return degrees(atan(opposite / adjacent))

  def adjust_angle_to_aim_direction(self, angle: Degree, aiming_down: bool, is_moving_right: bool) -> Radian:
    adjustment: Degree = 0
    if is_moving_right:
      if aiming_down:
        adjustment = 180 + 2 * (90 - angle)
    else:
      if aiming_down:
        adjustment = 180
      else:
        adjustment = 2 * (90 - angle)
    return radians(angle + adjustment)

  def get_line_length(self, adjacent, opposite) -> float:
    return sqrt(adjacent ** 2 + opposite ** 2)

  def get_release_speed(self, length) -> float:
    if length > 100:
      return ARROW_MAX_SPEED
    # Ex.: 80 / 100 = 80% * ARROW_MAX_SPEED
    return ARROW_MAX_SPEED * (length / 100)
