from math import atan, degrees, sqrt, sin, cos
from pygame import Surface, draw, mouse
from pygame.sprite import Sprite

from constants import ARROW_MAX_SPEED


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

	def set_center(self):
		if self.released:
			return
		x, y = self.character.get_center()
		self.rect.x = x
		self.rect.y = y

	def release(self, release_position):
		self.released = True
		click_x, click_y = self.click_position
		release_x, release_y = release_position
		print(click_x, click_y)
		print(release_x, release_y)
		# Those names might be fucked up
		adjacent = abs(click_x - release_x)
		opposite = abs(click_y - release_y)
		print(adjacent, opposite)
		# Get the angle
		angle = self.get_release_angle(adjacent, opposite)
		print("Angle ", angle)
		# Get line's length
		length = self.get_line_length(adjacent, opposite)
		print("Lenght", length)
		speed = self.get_release_speed(length)
		vel_x = cos(angle) * speed
		vel_y = sin(angle) * speed

	def update(self):
		pass

	def get_release_speed(self, length):
		if length > 100:
			return ARROW_MAX_SPEED
		# Ex.: 80 / 100 = 80% * ARROW_MAX_SPEED
		return ARROW_MAX_SPEED * (length / 100)

	def get_release_angle(self, adjacent, opposite):
		if adjacent == 0:
			adjacent = 90
		tangent = atan(opposite / adjacent)
		print("tang", tangent)
		return degrees(tangent)

	def get_line_length(self, adjacent, opposite):
		return sqrt(adjacent ** 2 + opposite ** 2)
