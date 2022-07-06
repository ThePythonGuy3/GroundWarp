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
	def __init__(self, animator, kill = False, half = False):
		self.animator = animator
		self.kill = kill
		self.half = half

	def create(self, colliderList, dimension, tilex, tiley, rotation): # Rotation goes in 0-3 format, 0 being upwards and going clockwise
		if self.half:
			for i in range(2):
				if rotation == 0: colliderList[dimension].append(col.collider(tilex * 2 + i, tiley * 2 + 1, self.kill))
				if rotation == 1: colliderList[dimension].append(col.collider(tilex * 2, tiley * 2 + i, self.kill))
				if rotation == 2: colliderList[dimension].append(col.collider(tilex * 2 + i, tiley * 2, self.kill))
				if rotation == 3: colliderList[dimension].append(col.collider(tilex * 2 + 1, tiley * 2 + i, self.kill))
		else:
			for i in range(2):
				for j in range(2):
					colliderList[dimension].append(col.collider(tilex * 2 + i, tiley * 2 + i, self.kill))

		return self

#0 is empty
blocks = [
	block(anim.animator(anim.sprite("block"))),                 #1 ---- A
	block(anim.animator(anim.split("block1", 6))),              #2
	block(anim.animator(anim.split("block2", 2), 3)),           #3
	block(anim.animator(anim.sprite("spoike")), True, True),    #4
	block(anim.animator(anim.sprite("blockB"))),                #5 ---- B
	block(anim.animator(anim.sprite("blockB1"))),               #6
	block(anim.animator(anim.split("blockB2", 9), 1, True)),             #7
	block(anim.animator(anim.split("spoikeB", 6)), True, True), #8
	block(anim.animator(anim.sprite("blockC"))),                #9 ---- C
	block(anim.animator(anim.sprite("blockC1"))),               #10
	block(anim.animator(anim.sprite("blockC2"))),               #11
	block(anim.animator(anim.sprite("spoikeC")), True, True)    #12
]

bitmask = anim.split("bitmask", 16)

colliderList = [[], [], []] # Dimensions A, B, C
tiles = [{}, {}, {}]
bitm = [{}, {}, {}]

def loadRoom(name):
	global colliderList, tiles, bitm

	colliderList = [[], [], []]
	tiles = [{}, {}, {}]
	bitm = [{}, {}, {}]

	ar = open("rooms/" + name + "/A.room", "r")
	br = open("rooms/" + name + "/B.room", "r")
	cr = open("rooms/" + name + "/C.room", "r")

	a = ar.read()
	b = br.read()
	c = cr.read()

	ar.close()
	br.close()
	cr.close()

	n = [a, b, c]

	for r in range(3):
		x = 0
		y = 0
		for i in n[r]:
			if i == ";":
				x = -1
				y += 1
			else:
				v = int(i)
				if v != 0:
					tiles[r][(x, y)] = blocks[v - 1].create(colliderList, r, x, y, 0)
			x += 1

	for r in range(3):
		dd = tiles[r].keys()
		for i in dd:
			if tiles[r][i].kill:
				bitm[r][i] = 15
				continue

			x, y = i
			bt = 0

			if (x, y - 1) in dd: bt += 1
			if (x - 1, y) in dd: bt += 2
			if (x + 1, y) in dd: bt += 4
			if (x, y + 1) in dd: bt += 8

			bitm[r][i] = bt

def mainGame(display):
	global colliderList, tiles, bitm

	running = True

	tickF = tick = 0
	deltaTime = 1

	gameTimeStart = time()
	preGameTime = gameTimeStart

	mainSurf = pg.Surface((960, 640), pg.SRCALPHA, 32)

	while running:
		for e in pg.event.get():
			if e.type == pg.QUIT:
				running = False

		gameTime = time() - gameTimeStart
		deltaTime = (gameTime * 60 - preGameTime * 60)

		display.fill((255, 255, 255))

		for i in tiles[0].keys():
			mainSurf.blit(tiles[0][i].animator.animate(tick), (i[0] * 32, i[1] * 32))
			mainSurf.blit(bitmask[bitm[0][i]], (i[0] * 32, i[1] * 32))

		for i in range(960):
			for j in range(640):
				if mainSurf.get_at((i, j)) == (0, 0, 0, 255):
					mainSurf.set_at((i, j), (0, 0, 0, 0))

		display.blit(mainSurf, (0, 0))
		pg.display.update()

		tickF += deltaTime
		tick = int(tickF)
		preGameTime = gameTime

loadRoom("room1")
mainGame(display)

pg.quit()