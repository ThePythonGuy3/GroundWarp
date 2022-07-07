from math import *
pg = None

class animator:
	def __init__(self, sprites, speed = 1, pingpong = False):
		self.sprites = sprites
		self.speed = speed
		self.pingpong = pingpong

	def animate(self, tick):
		if type(self.sprites) != list: return self.sprites
		tickP = int((tick / 60) * self.speed * pi) % len(self.sprites)
		if self.pingpong: tickP = int(round(abs(sin(tick / 60 * (self.speed))) * (len(self.sprites) - 1)))
		return self.sprites[tickP]

def split(name, n):
	img = pg.image.load("sprites/" + name + ".png")
	output = []
	for i in range(n):
		surf = pg.Surface((16, 16), pg.SRCALPHA, 32)
		surf.blit(img, (0, 0), (i * 16, 0, 16, 16))
		img2 = pg.transform.scale(surf, (32, 32))
		output.append(img2)
	return output

def sprite(name):
	img = pg.image.load("sprites/" + name + ".png").convert_alpha()
	img = pg.transform.scale2x(img)
	return img
