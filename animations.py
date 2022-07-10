from math import *
pg = None

class animator:
	def __init__(self, sprites, speed = 1, pingpong = False):
		self.sprites = sprites
		self.speed = speed
		self.pingpong = pingpong #animation going back and forth or nah
		self.lastFrame = -1
		self.currentAnimationFrame = -1
		self.animated = (type(self.sprites) == list)

	def updateAnimationFrame(self, tick):
		if self.animated:
			self.currentAnimationFrame = int((tick / 60) * self.speed * pi) % len(self.sprites)
			if self.pingpong: self.currentAnimationFrame = int(round(abs(sin(tick / 60 * (self.speed))) * (len(self.sprites) - 1)))

	def animationCheck(self):
		if not self.animated: return False
		return self.lastFrame != self.currentAnimationFrame

	def animate(self):
		if not self.animated: return self.sprites
		return self.sprites[self.currentAnimationFrame]

def split(name, n):
	img = pg.image.load("sprites/" + name + ".png")
	output = []
	for i in range(n):
		surf = pg.Surface((16, 16), pg.SRCALPHA, 32)
		surf.blit(img, (0, 0), (i * 16, 0, 16, 16))
		img2 = pg.transform.scale(surf, (32, 32))
		output.append(img2)
	return output

def scale2x(surf):
	return pg.transform.scale(surf, (surf.get_size()[0] * 2, surf.get_size()[1] * 2))


def sprite(name):
	img = pg.image.load("sprites/" + name + ".png").convert_alpha()
	w, h = img.get_size()
	img = pg.transform.scale(img, (w * 2, h * 2))
	return img
