from math import atan2, degrees, sqrt, sin, cos
from pygame import Surface, draw, mouse
from pygame.sprite import Sprite

from constants import ARROW_MAX_SPEED, FLOOR_Y


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
		self.angle = None
		self.t = 0

	def set_center(self):
		if self.released:
			return
		x, y = self.character.get_center()
		self.rect.x = x
		self.rect.y = y

	def release(self, release_position):
		if self.released:
			return
		self.released = True
		click_x, click_y = self.click_position
		self.release_position = release_x, release_y = release_position
		# Those names might be fucked up
		adjacent = abs(release_x -  click_x)
		opposite = abs(release_y -  click_y)
		print(adjacent, opposite)
		#print(adjacent, opposite)
		# Get the angle
		self.angle = self.get_release_angle(adjacent, opposite)
		if click_y > release_y:
			self.angle = -self.angle
		print("angle", self.angle)
		#print("Angle ", self.angle)
		# Get line's length
		length = self.get_line_length(adjacent, opposite)
		#print("Lenght", length)
		if not self.release_speed:
			self.release_speed = self.get_release_speed(length)

	def update(self):
		if self.rect.y >= FLOOR_Y or not self.released:
			return
		angle = 45
		speed = 4
		g = 0.980

		vx = cos(self.angle) * speed
		vy = -sin(self.angle) * speed + g * self.t
		if self.rect.y < 10:
			vy = +sin(angle) * speed + (0.5 * g * self.t * self.t)
		self.rect.x += vx
		self.rect.y += vy
		self.t += 0.1
		#print(self.rect.center)
		#print(self.t)

	def get_release_speed(self, length):
		if length > 100:
			return ARROW_MAX_SPEED
		# Ex.: 80 / 100 = 80% * ARROW_MAX_SPEED
		return ARROW_MAX_SPEED * (length / 100)

	def get_release_angle(self, adjacent, opposite):
		if adjacent == 0:
			adjacent = 90
		tangent = atan2(opposite, adjacent)
		#print("tang", tangent)
		return -degrees(tangent)

	def get_line_length(self, adjacent, opposite):
		return sqrt(adjacent ** 2 + opposite ** 2)
