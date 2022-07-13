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

	def copy(self):
		return animator(self.sprites, self.speed, self.pingpong)

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

	def getFirstFrame(self):
		if self.animated: return self.sprites[0]
		else: return self.sprites

def split(name, n):
	img = pg.image.load("sprites/" + name + ".png")
	output = []
	for i in range(n):
		surf = pg.Surface((16, 16), pg.SRCALPHA, 32)
		surf.blit(img, (0, 0), (i * 16, 0, 16, 16))
		img2 = pg.transform.scale(surf, (32, 32))
		output.append(img2)
	return output

def splitCustom(name, n, width, height, flipHorizontally = False, flipVertically = False):
	img = pg.image.load("sprites/" + name + ".png")
	output = []
	for i in range(n):
		surf = pg.Surface((width, height), pg.SRCALPHA, 32)
		surf.blit(img, (0, 0), (i * width, 0, width, height))
		img2 = pg.transform.scale(surf, (width * 2, height * 2))
		output.append(pg.transform.flip(img2, flipHorizontally, flipVertically))
	return output

def sprite(name, flipHorizontally = False, flipVertically = False):
	img = pg.image.load("sprites/" + name + ".png").convert_alpha()
	w, h = img.get_size()
	img = pg.transform.scale(img, (w * 2, h * 2))
	return pg.transform.flip(img, flipHorizontally, flipVertically)

def blurSurf(surface, amt):
    if amt < 1.0:
        raise ValueError("Arg 'amt' must be greater than 1.0, passed in value is %s"%amt)
    scale = 1.0/float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf