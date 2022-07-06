import pygame as pg
from math import *
from time import *
from random import *

import animations as anim
import collisions as col

anim.pg = pg
col.pg = pg

pg.init()
display = pg.display.set_mode((960, 640))

class block:
	def __init__(self, animators, kill = False, half = False):
		self.animators = animators # Array of three, one per dimension
		self.kill = kill
		self.half = half

	def create(self, colliderList, dimension, tilex, tiley, rotation): # Rotation goes in 0-3 format, 0 being upwards and going clockwise
		if half:
			for i in range(2):
				if rotation == 0: colliderList[dimension].append(col.collider(tilex * 2 + i, tiley * 2 + 1, self.kill))
				if rotation == 1: colliderList[dimension].append(col.collider(tilex * 2, tiley * 2 + i, self.kill))
				if rotation == 2: colliderList[dimension].append(col.collider(tilex * 2 + i, tiley * 2, self.kill))
				if rotation == 3: colliderList[dimension].append(col.collider(tilex * 2 + 1, tiley * 2 + i, self.kill))
		else:
			for i in range(2):
				for j in range(2):
					colliderList[dimension].append(col.collider(tilex * 2 + i, tiley * 2 + i, self.kill))

#0 is empty
blocks = [
	block(anim.animator(anim.sprite("block"))),     #1
	block(anim.animator(anim.split("block1", 6))),  #2
	block(anim.animator(anim.split("block2", 2))),  #3
	block(anim.animator(anim.sprite("spoike"))),    #4
	block(anim.animator(anim.sprite("blockB"))),    #5
	block(anim.animator(anim.sprite("blockB1"))),   #6
	block(anim.animator(anim.split("blockB2", 9))), #7
	block(anim.animator(anim.split("spoikeB", 6))), #8
	block(anim.animator(anim.sprite("blockC"))),    #9
	block(anim.animator(anim.sprite("blockC1"))),   #10
	block(anim.animator(anim.sprite("spoikeC")))    #11
]

def mainGame(display):
	running = True

	tickF = tick = 0
	deltaTime = 1

	gameTimeStart = time()
	preGameTime = gameTimeStart

	tiles = [[0 for i in range(30)] for j in range(20)]

	for i in range(len(tiles)):
		if randint(0, 6) >= 3:
			tiles[i] = 1

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

organicSpike = anim.animator(anim.split("block1", 6), 3)

colliderList = [[], [], []] # Dimensions A, B, C

mainGame(display)

pg.quit()