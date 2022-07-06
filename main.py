import pygame as pg
from math import *
from time import *

from animations import *

size = 30 # Tilespace 0-29   Colliderspace 0-59
colliderList = [[], [], []] # Dimensions A, B, C

class collider:
	def __init__(self, x, y, kill):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.kill = kill

class block:
	def __init__(self, key, animators, kill, half = False):
		self.key = key
		self.animators = animators # Array of three, one per dimension
		self.kill = kill
		self.half = half

	def create(self, dimension, tilex, tiley, rotation): # Rotation goes in 0-3 format, 0 being upwards and going clockwise
		if not half:
			for i in range(2):
				for j in range(2):
					colliderList[dimension].append(collider(tilex * 2 + i, tiley * 2 + i, self.kill))
		else:
			for i in range(2):
				if rotation == 0: colliderList[dimension].append(collider(tilex * 2 + i, tiley * 2 + 1, self.kill))
				if rotation == 1: colliderList[dimension].append(collider(tilex * 2, tiley * 2 + i, self.kill))
				if rotation == 2: colliderList[dimension].append(collider(tilex * 2 + i, tiley * 2, self.kill))
				if rotation == 3: colliderList[dimension].append(collider(tilex * 2 + 1, tiley * 2 + i, self.kill))

def sprite(name):
	img = pg.image.load("sprites/" + name + ".png").convert_alpha()
	img = pg.transform.scale(img, (32, 32))
	return img

global organicSpike

def mainGame(display):
	running = True

	tickF = tick = 0
	deltaTime = 1

	gameTimeStart = time()
	preGameTime = gameTimeStart
	while running:
		for e in pg.event.get():
			if e.type == pg.QUIT:
				running = False

		gameTime = time() - gameTimeStart
		deltaTime = (gameTime * 60 - preGameTime * 60)

		display.fill((255, 255, 255))


		for i in range(30):
			for j in range(20):
				display.blit(organicSpike.animate(tick), (i * 32, j * 32))

		pg.display.update()

		tickF += deltaTime
		tick = int(tickF)
		preGameTime = gameTime

pg.init()
display = pg.display.set_mode((960, 640))

organicSpike = animator(split(pg, "block1", 6), 3)
print(organicSpike.sprites)
mainGame(display)

pg.quit()