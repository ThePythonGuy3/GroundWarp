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
	block(anim.animator(anim.split("blockB2", 9), 2, True)),    #7
	block(anim.animator(anim.split("spoikeB", 6), 2), True, True), #8
	block(anim.animator(anim.sprite("blockC"))),                #9 ---- C
	block(anim.animator(anim.sprite("blockC1"))),               #10
	block(anim.animator(anim.sprite("blockC2"))),               #11
	block(anim.animator(anim.sprite("spoikeC")), True, True)    #12
]

bitmask = anim.split("bitmask", 16)

colliderList = [[], [], []] # Dimensions A, B, C
tiles = [{}, {}, {}]
bitm = [{}, {}, {}]

bg = pg.image.load("sprites/bg.png")
logo = anim.sprite("logo")
crtag = anim.sprite("creditsTag")
playB = anim.sprite("play")
playBH = anim.sprite("play-hover")
playBP = anim.sprite("play-press")
exitB = anim.sprite("exit")
exitBH = anim.sprite("exit-hover")
exitBP = anim.sprite("exit-press")

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

	nn = [pg.Surface((30, 20), pg.SRCALPHA, 32) for i in range(3)]

	rx, ry = -1, -1
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
					if v == 9:
						rx = x
						ry = y
					else: tiles[r][(x, y)] = blocks[v - 1 + r * 4].create(colliderList, r, x, y, 0)
			x += 1

	for r in range(3):
		dd = tiles[r].keys()
		for i in dd:
			if tiles[r][i].kill:
				bitm[r][i] = 15
				continue

			x, y = i
			bt = 0
			sdbt = 0

			if (x, y - 1) in dd:
				bt += 1
				if not tiles[r][(x, y - 1)].kill: sdbt += 1
			elif y - 1 < 0:
				bt += 1
				sdbt += 1

			if (x - 1, y) in dd:
				bt += 2
				if not tiles[r][(x - 1, y)].kill: sdbt += 2
			elif x - 1 < 0:
				bt += 2
				sdbt += 2

			if (x + 1, y) in dd:
				bt += 4
				if not tiles[r][(x + 1, y)].kill: sdbt += 4
			elif x + 1 > 29:
				bt += 4
				sdbt += 4

			if (x, y + 1) in dd:
				bt += 8
				if not tiles[r][(x, y + 1)].kill: sdbt += 8
			elif y + 1 > 19:
				bt += 8
				sdbt += 8



			if sdbt == 15: nn[r].set_at((x, y), (0, 0, 0))

			bitm[r][i] = bt

	for i in range(len(nn)):
		nn[i] = pg.transform.smoothscale(nn[i], (960, 640))

	return rx, ry, nn

def blitRotateCenter(surf, image, angle, position, scale):
	rotated_image = pg.transform.rotate(image, angle)
	w, h = rotated_image.get_size()
	rotated_image = pg.transform.scale(rotated_image, (int(w * scale), int(h * scale)))
	new_rect = rotated_image.get_rect(center = image.get_rect().center)

	nnR = pg.Rect(new_rect.x + position[0], new_rect.y + position[1], new_rect.w, new_rect.h)

	surf.blit(rotated_image, nnR)

def mainMenu(display):
	pg.mixer.music.stop()
	pg.mixer.music.unload()
	pg.mixer.music.load("audio/music/menu.mp3")
	pg.mixer.music.play(loops=-1, fade_ms=300)

	running = True

	tickF = tick = 0
	deltaTime = 1

	gameTimeStart = time()
	preGameTime = gameTimeStart
	fullR = False
	hoverP = False
	hoverE = False

	playBRect = pg.Rect(960 // 2 - 64, 640 // 2 - 40, 128, 64)
	exitBRect = pg.Rect(960 // 2 - 64, 640 // 2 + 40, 128, 64)
	st = 210

	while running:
		pressed = False
		for e in pg.event.get():
			if e.type == pg.QUIT:
				running = False
				fullR = True
			if e.type == pg.KEYDOWN:
				if e.key == pg.K_k:
					running = False
			if e.type == pg.MOUSEBUTTONDOWN:
				if e.button == 1: pressed = True

		gameTime = time() - gameTimeStart
		deltaTime = (gameTime * 60 - preGameTime * 60)

		msx, msy = pg.mouse.get_pos()

		display.fill((255, 255, 255))
		display.blit(bg, (0, 0))
		blitRotateCenter(display, logo, sin(tick / 60) * 6, (960 // 2 - 176 * 2, 40), 1 + ((sin(tick / 30) + 1) / 2) * 0.3)
		display.blit(crtag, (960 - 270, 640 - 22))

		pbTex = playB
		if playBRect.collidepoint(msx, msy):
			pbTex = playBH
			if pressed:
				pbTex = playBP
				running = False
		display.blit(pbTex, (playBRect.x, playBRect.y))
		ebTex = exitB
		if exitBRect.collidepoint(msx, msy):
			ebTex = exitBH
			if pressed:
				ebTex = exitBP
				running = False
				fullR = True
		display.blit(ebTex, (exitBRect.x, exitBRect.y))

		if st >= 0:
			pg.draw.rect(display, (0, 0, 0), pg.Rect(0, 0, 960, int(((st / 200) ** 2) * 320)))
			pg.draw.rect(display, (0, 0, 0), pg.Rect(0, 640 -int(((st / 200) ** 2) * 320), 960, int(((st / 200) ** 2) * 320)))
			st -= 5

		pg.display.update()

		tickF += deltaTime
		tick = int(tickF)
		preGameTime = gameTime

	pg.mixer.music.fadeout(300)
	if not fullR:
		for i in range(211):
			pg.event.get()
			pg.draw.rect(display, (0, 0, 0), pg.Rect(0, 0, 960, int(((i / 200) ** 2) * 320)))
			pg.draw.rect(display, (0, 0, 0), pg.Rect(0, 640 -int(((i / 200) ** 2) * 320), 960, int(((i / 200) ** 2) * 320)))
			pg.display.update()
			pg.time.delay(5)

		pg.time.delay(1000)
		mainGame(display)


def mainGame(display):
	global colliderList, tiles, bitm

	running = True

	tickF = tick = 0
	deltaTime = 1

	px, py, sh = loadRoom("room1")
	px *= 32
	py *= 32

	gameTimeStart = time()
	preGameTime = gameTimeStart

	enableShadow = False

	mainSurf = pg.Surface((960, 640), pg.SRCALPHA, 32)
	shad = anim.sprite("shadow")
	glow = anim.sprite("glow")

	dimension = 0
	st = 210

	while running:
		for e in pg.event.get():
			if e.type == pg.QUIT:
				running = False
			if e.type == pg.KEYDOWN:
				if e.key == pg.K_RIGHT:
					dimension += 1
					px += 1
				if e.key == pg.K_LEFT:
					dimension -= 1
					px -= 1

				dimension %= 3

		gameTime = time() - gameTimeStart
		deltaTime = (gameTime * 60 - preGameTime * 60)

		display.fill((255, 255, 255))
		display.blit(bg, (0, 0))
		mainSurf.fill((0, 0, 0, 0))

		if enableShadow:
			shadowSurf.fill((16, 16, 16))
			shadowSurf.blit(shad, (px - 16*5, py - 16*5))

		for i in tiles[dimension].keys():
			mainSurf.blit(tiles[dimension][i].animator.animate(tick), (i[0] * 32, i[1] * 32))
			mainSurf.blit(bitmask[bitm[dimension][i]], (i[0] * 32, i[1] * 32), special_flags=pg.BLEND_RGBA_MULT)

		mainSurf.blit(shad, (px, py + 8), special_flags=pg.BLEND_RGBA_MULT)

		display.blit(glow, (px - 32, py - 32))
		display.blit(mainSurf, (0, 0))
		display.blit(anim.sprite("playAr"), (px, py - 16))
		display.blit(sh[dimension], (0, 0))

		if st >= 0:
			pg.draw.rect(display, (0, 0, 0), pg.Rect(0, 0, 960, int(((st / 200) ** 2) * 320)))
			pg.draw.rect(display, (0, 0, 0), pg.Rect(0, 640 -int(((st / 200) ** 2) * 320), 960, int(((st / 200) ** 2) * 320)))
			st -= 5

		pg.display.update()

		tickF += deltaTime
		tick = int(tickF)
		preGameTime = gameTime

mainMenu(display)

for i in range(211):
	pg.event.get()
	pg.draw.rect(display, (0, 0, 0), pg.Rect(0, 0, 960, int(((i / 200) ** 2) * 320)))
	pg.draw.rect(display, (0, 0, 0), pg.Rect(0, 640 -int(((i / 200) ** 2) * 320), 960, int(((i / 200) ** 2) * 320)))
	pg.display.update()
	pg.time.delay(5)

pg.quit()