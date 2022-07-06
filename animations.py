from math import *

class animator:
	def __init__(self, sprites, speed, pingpong = False):
		self.sprites = sprites
		self.speed = speed
		self.pingpong = pingpong

	def animate(self, tick):
		if len(self.sprites) == 1: return self.sprites[0]
		tickP = int((tick / 60) * self.speed * pi) % len(self.sprites)
		if self.pingpong: tickP = int(round(abs(sin(tick / 60 * (self.speed))) * (len(self.sprites) - 1)))
		return self.sprites[tickP]

def split(pg, name, n):
	img = pg.image.load("sprites/" + name + ".png")
	output = []
	for i in range(n):
		surf = pg.Surface((16, 16), pg.SRCALPHA, 32)
		surf.blit(img, (0, 0), (i * 16, 0, 16, 16))
		img2 = pg.transform.scale(surf, (32, 32))
		output.append(img2)
	return output
