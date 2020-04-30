from pygame import Surface, draw, mouse
from pygame.sprite import Sprite


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
