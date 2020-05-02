from pygame import Surface, draw, mouse
from pygame.sprite import Sprite

from constants import (
	CHARACTER_WIDTH,
	CHARACTER_HEIGHT,
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
		self.image = Surface([width, height])
		self.image.fill(color)
		draw.rect(self.image, color, [0, 0, width, height])
		# Instead we could load a proper pciture of a car..	.
		# self.image = pygame.image.load("car.png").convert_alpha()
		# Fetch the rectangle object that has the dimensions of the image.
		self.rect = self.image.get_rect()

		self.is_jumping = False
		self.jumpCnt = CHARACTER_JUMP_FRAMES
		self.screen = screen

	def get_center(self):
		return self.rect.center

	def collidepoint(self, position):
		return self.rect.collidepoint(position) == 1

	def move_left(self):
		self.rect.move_ip(-1 * CHARACTER_SPEED, 0)

	def move_right(self):
		self.rect.move_ip(1 * CHARACTER_SPEED, 0)

	def jump(self):
		if not self.is_jumping:
			self.is_jumping = True

	def perform_jump(self):
		if self.jumpCnt >= -CHARACTER_JUMP_FRAMES:
			self.rect.y -= (self.jumpCnt * abs(self.jumpCnt)) * 0.5
			self.jumpCnt -= 1
		else:
			self.jumpCnt = CHARACTER_JUMP_FRAMES
			self.draw_character_on_the_floor()
			self.is_jumping = False

	def draw_character_on_the_floor(self):
		self.rect.y = FLOOR_Y - CHARACTER_HEIGHT

	def draw_mouse(self):
		mouse_pos = mouse.get_pos()
		pos = (self.rect.x, self.rect.y)
		draw.line(self.screen, self.color, pos, mouse_pos, 5)		
