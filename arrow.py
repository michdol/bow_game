from math import degrees, sqrt, sin, cos, tan, radians
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
		self.is_moving_right = False
		self.stopped = False

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
		if release_x < click_x:
			self.is_moving_right = True
		# Those names might be fucked up
		adjacent = abs(release_x -  click_x)
		opposite = abs(release_y -  click_y)
		self.angle = self.get_release_angle(adjacent, opposite)
		aiming_down = release_y < click_y
		if self.is_moving_right:
			if aiming_down:
				self.angle += radians(90 * 3)
		else:
			if aiming_down:
				self.angle += radians(90 * 2)
		#print(self.angle, adjacent, opposite)
		length = self.get_line_length(adjacent, opposite)
		self.release_speed = self.get_release_speed(length)
		print("\nrelease\n\n\n\n")

	def update(self):
		if self.rect.y >= FLOOR_Y:
			self.stopped = True
		if not self.released:
			return
		speed = self.release_speed
		t = self.t
		g = 0.980

		vx = speed
		vy = -sin(self.angle) * speed + 0.5 * g * t * t
		print("angle {} -sin(angle) {:0<25} 0.5 * g * t * t {:0<25}".format(self.angle, -sin(self.angle), 0.5*g*t*t))

		if self.is_moving_right:
			self.rect.x += vx
		else:
			self.rect.x -= vx
		self.rect.y += vy
		self.t += 0.1

	def get_release_speed(self, length):
		if length > 100:
			return ARROW_MAX_SPEED
		# Ex.: 80 / 100 = 80% * ARROW_MAX_SPEED
		return ARROW_MAX_SPEED * (length / 100)

	def get_release_angle(self, adjacent, opposite):
		tangent = tan(opposite / adjacent)
		print(adjacent, opposite)
		print(tangent)
		angle = degrees(tangent)
		print(angle)
		return tangent

	def get_line_length(self, adjacent, opposite):
		return sqrt(adjacent ** 2 + opposite ** 2)
