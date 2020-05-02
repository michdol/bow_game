from math import atan2, degrees, sqrt, sin, cos

from pygame import Surface, draw, mouse, font
from pygame.sprite import Sprite


green = (0, 255, 0)
blue = (0, 0, 128)

class AimLine(Sprite):
	def __init__(self, color, width, height, screen, character):
		Sprite.__init__(self)
		self.color = color
		self.image = Surface([width, height])
		self.image.set_colorkey(color)
		self.screen = screen
		self.character = character

	def draw(self, start):
		mouse_keys = mouse.get_pressed()
		if mouse_keys[0]:
			mouse_pos = mouse.get_pos()
			draw.line(self.screen, self.color, start, mouse_pos, 5)
			self.text(*start)
			self.text(*mouse_pos)
			self.angle(start, mouse_pos)

	def text(self, x, y):
		font_ = font.Font('freesansbold.ttf', 32) 
		text_ = "({}, {})".format(x, y)
		text = font_.render(text_, True, green, blue) 
		rect = text.get_rect()
		rect.x = x + 50
		rect.y = y
		self.screen.blit(text, rect)

	def angle(self, start, end):
		adjacent, opposite = self.get_triangle_sides(start, end)
		angle = self.get_release_angle(adjacent, opposite)
		if start[1] > end[1]:
			angle = -angle
		font_ = font.Font('freesansbold.ttf', 15) 
		text_ = "({}°)".format(angle)
		text = font_.render(text_, True, green, blue) 
		rect = text.get_rect()
		rect.x = start[0]
		rect.y = start[1] + 50
		self.screen.blit(text, rect)

	def get_triangle_sides(self, start, end):
		start_x, start_y = start
		end_x, end_y = end
		return abs(start_x - end_x), abs(start_y - end_y)

	def get_release_angle(self, adjacent, opposite):
		if adjacent == 0:
			adjacent = 90
		tangent = atan2(opposite, adjacent)
		#print("tang", tangent)
		return -degrees(tangent)