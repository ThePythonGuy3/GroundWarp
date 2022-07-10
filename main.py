import pygame as pg
from math import *
from time import *
from random import *
import os
import webbrowser

import animations as anim
import collisions as col

anim.pg = pg
col.pg = pg

editorURL = "file:///" + os.getcwd() + "/editor/index.html"

def openEditor():
	webbrowser.open_new_tab(editorURL)

pg.init()
display = pg.display.set_mode((960, 640))
pg.display.set_caption("GroundWarp")
pg.display.set_icon(anim.sprite("icon"))

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
			colliderList[dimension].append(col.collider(tilex * 2, tiley * 2, self.kill, 32))

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

backgrounds = [anim.sprite("factorybg"), anim.sprite("factorybg"), anim.sprite("factorybg")]
crtag = anim.sprite("creditsTag")

playB = anim.sprite("play")
playBH = anim.sprite("play-hover")
playBP = anim.sprite("play-press")

exitB = anim.sprite("exit")
exitBH = anim.sprite("exit-hover")
exitBP = anim.sprite("exit-press")

makeB = anim.sprite("make")
makeBH = anim.sprite("make-hover")
makeBP = anim.sprite("make-press")

snek = anim.animator(anim.split("gamesnek", 11), 2)
snakeask = anim.sprite("snakeask")
snektext = anim.split("snake", 5)
snekfx = [pg.mixer.Sound("audio/sfx/snek" + str(i + 1) + ".mp3") for i in range(4)]
coll = anim.sprite("collider")
collkill = anim.sprite("colliderkill")

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

			if (x - 1, y) in dd and not tiles[r][(x - 1, y)].kill:
				bt += 2
				if not tiles[r][(x - 1, y)].kill: sdbt += 2
			elif x - 1 < 0:
				bt += 2
				sdbt += 2

			if (x + 1, y) in dd and not tiles[r][(x + 1, y)].kill:
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

def inOutQuadBlend(t):
	if t <= 0.5:
		return 2.0 * t * t
	t -= 0.5
	return 2.0 * t * (1.0 - t) + 0.5

loops = ["audio/music/loop1.mp3"]
def mainMenu(display):
	pg.mixer.music.stop()
	pg.mixer.music.unload()
	pg.mixer.music.load("audio/music/menu.mp3")
	pg.mixer.music.play(loops=-1, fade_ms=300)

	logo = anim.sprite("logo")

	running = True

	tickF = tick = 0
	deltaTime = 1

	gameTimeStart = time()
	preGameTime = gameTimeStart
	fullR = False
	hoverP = False
	hoverE = False

	playBRect = pg.Rect(960 // 2 - 64, 640 // 2 - 40, 128, 64)
	exitBRect = pg.Rect(960 // 2 - 64, 640 // 2 + 120, 128, 64)
	makeBRect = pg.Rect(960 // 2 - 64, 640 // 2 + 40, 128, 64)
	st = 210

	snake = [pg.K_s, pg.K_n, pg.K_a, pg.K_k, pg.K_e]
	snakeProg = 0
	snakeEnable = True
	snakes = []
	timeTrigger = True
	snangle = 0

	while running:
		pressed = False
		for e in pg.event.get():
			if e.type == pg.QUIT:
				running = False
				fullR = True
			if e.type == pg.KEYDOWN:
				if snakeEnable:
					if e.key == snake[snakeProg]:
						snakeProg += 1
						if snakeProg >= 5:
							pg.mixer.music.stop()
							pg.mixer.music.unload()
							pg.mixer.music.load("audio/music/snak.mp3")
							pg.mixer.music.play(loops=-1, fade_ms=300)

							snakeEnable = False
					else:
						snakeProg = 0
			if e.type == pg.MOUSEBUTTONDOWN:
				if e.button == 1: pressed = True

		gameTime = time() - gameTimeStart
		deltaTime = (gameTime * 60 - preGameTime * 60)

		msx, msy = pg.mouse.get_pos()

		display.fill((255, 255, 255))
		if not snakeEnable:
			if len(snakes) < 1000:
				snakes.append((randint(0, 960), randint(0, 640), randint(0, 360), randint(0, 90)))
			for i in snakes:
				blitRotateCenter(display, snek.animate(tick + i[3]), i[2], i[:2:], 1)
			if not (int(time() * 2) % 2):
				timeTrigger = True

			if timeTrigger and int(time() * 2) % 2:
				timeTrigger = False
				choice(snekfx).play()

		for i in range(snakeProg):
			display.blit(snektext[i], (i * 32 + 2, 640 - 34))

		if not snakeEnable and snangle < 180:
			snangle += 2

		if snangle >= 90:
			logo = anim.sprite("logo-snake")

		display.blit(snakeask, (0, 0))
		easeang = inOutQuadBlend(snangle / 180)
		blitRotateCenter(display, logo, sin(tick / 60) * 6 - (360 * 2 + 180) * easeang, (960 // 2 - 176 * 2, 40), 1 + ((sin(tick / 30) + 1) / 2) * 0.3)
		display.blit(crtag, (960 - 270, 640 - 22))

		pbTex = playB
		if playBRect.collidepoint(msx, msy):
			pbTex = playBH
			if pressed:
				pbTex = playBP
				running = False
		blitRotateCenter(display, pbTex, (180) * easeang, (playBRect.x, playBRect.y), 1)
		mbTex = makeB
		if makeBRect.collidepoint(msx, msy):
			mbTex = makeBH
			if pressed:
				mbTex = makeBP
				openEditor()
		blitRotateCenter(display, mbTex, (180) * easeang, (makeBRect.x, makeBRect.y), 1)
		ebTex = exitB
		if exitBRect.collidepoint(msx, msy):
			ebTex = exitBH
			if pressed:
				ebTex = exitBP
				running = False
				fullR = True
		blitRotateCenter(display, ebTex, (180) * easeang, (exitBRect.x, exitBRect.y), 1)

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

blocksBuffer = pg.Surface((960, 640), pg.SRCALPHA, 32)
bg = pg.Surface((960, 640))

def generateBlocksBuffer(tiles, dimension, tick):
	global blocksBuffer
	blocksBuffer.fill((0, 0, 0, 0))
	for i in tiles[dimension].keys():
		blocksBuffer.blit(tiles[dimension][i].animator.animate(), (i[0] * 32, i[1] * 32))
		blocksBuffer.blit(bitmask[bitm[dimension][i]], (i[0] * 32, i[1] * 32), special_flags=pg.BLEND_RGBA_MULT)

def updateBlocksBuffer(tiles, dimension, tick):
	global blocksBuffer
	for i in tiles[dimension].keys():
		tiles[dimension][i].animator.updateAnimationFrame(tick)

		if tiles[dimension][i].animator.animationCheck():
			blocksBuffer.blit(tiles[dimension][i].animator.animate(), (i[0] * 32, i[1] * 32))
			blocksBuffer.blit(bitmask[bitm[dimension][i]], (i[0] * 32, i[1] * 32), special_flags=pg.BLEND_RGBA_MULT)

def updateBackground(dimension):
	global bg
	bg.blit(backgrounds[dimension], (0, 0))




def mainGame(display):
	global colliderList, tiles, bitm, blocksBuffer

	pg.mixer.music.fadeout(300)
	pg.mixer.music.load(choice(loops))
	pg.mixer.music.play(loops=-1, fade_ms=300)

	debug = False
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

	topBox = pg.Rect(0, 0, 20, 6)
	toppestBox = pg.Rect(0, 0, 20, 6)
	bottomBox = pg.Rect(0, 0, 20, 6)
	bottomestBox = pg.Rect(0, 0, 20, 6)
	rightBox = pg.Rect(0, 0, 6, 24)
	rightestBox = pg.Rect(0, 0, 6, 24)
	leftBox = pg.Rect(0, 0, 6, 24)
	leftestBox = pg.Rect(0, 0, 6, 24)
	killBox = pg.Rect(0, 0, 12, 18)

	hitboxes = [topBox, toppestBox, bottomBox, bottomestBox, rightBox, rightestBox, leftBox, leftestBox, killBox]

	dimension = 0
	st = 210

	speed = 1.5
	a = 0.3
	vx = 2
	vy = 8

	wpressed = False

	coyote = 0

	frame = 0

	retrigger = True

	generateBlocksBuffer(tiles, dimension, tick)

	updateBackground(dimension)

	while running:
		for e in pg.event.get():
			if e.type == pg.QUIT:
				running = False

			if e.type == pg.KEYDOWN:
				if e.key == pg.K_p:
					debug = not debug

				dimension %= 3

		gameTime = time() - gameTimeStart
		deltaTime = (gameTime * 60 - preGameTime * 60)

		topBox.x = px + 6
		topBox.y = py - 2
		toppestBox.x = px + 6
		toppestBox.y = py - 1
		bottomBox.x = px + 6
		bottomBox.y = py + 28
		bottomestBox.x = px + 6
		bottomestBox.y = py + 27
		leftBox.x = px + 4
		leftBox.y = py + 4
		leftestBox.x = px + 5
		leftestBox.y = py + 4
		rightBox.x = px + 22
		rightBox.y = py + 4
		rightestBox.x = px + 21
		rightestBox.y = py + 4
		killBox.x = px + 10
		killBox.y = py + 10

		rightCol = col.rectCollide(colliderList[dimension], rightBox, True)
		rightestCol = col.rectCollide(colliderList[dimension], rightestBox, True)
		leftCol = col.rectCollide(colliderList[dimension], leftBox, True)
		leftestCol = col.rectCollide(colliderList[dimension], leftestBox, True)
		topCol = col.rectCollide(colliderList[dimension], topBox, True)
		toppestCol = col.rectCollide(colliderList[dimension], toppestBox, True)
		bottomCol = col.rectCollide(colliderList[dimension], bottomBox, True)
		bottomestCol = col.rectCollide(colliderList[dimension], bottomestBox, True)
		killCol = col.rectCollide(colliderList[dimension], killBox)

		cols = [topCol, toppestCol, bottomCol, bottomestCol, rightCol, rightestCol, leftCol, leftestCol, killCol]

		if bottomCol[0]: coyote = 20

		lp = False
		rp = False
		if pg.key.get_pressed()[pg.K_d]:
			vx += a * speed
			rp = True
		if pg.key.get_pressed()[pg.K_a]:
			vx -= a * speed
			lp = True
		if pg.key.get_pressed()[pg.K_w]:
			if not wpressed and (bottomCol[0] or rightCol[0] or leftCol[0] or coyote > 0):
				if not bottomCol[0] and coyote == 0:
					if rightCol[0]:
						vx = -12
					else: vx = 12
				vy = -6

			wpressed = True
		else:
			wpressed = False

		if vy < 9.8:
			ama = a
			if vy > 0 and ((rightCol[0] and rp) or (leftCol[0] and lp)): ama = a / 5
			vy += ama

		if rightCol[0] and vx > 0: vx = 0
		if rightestCol[0]: vx = -0.5
		if leftCol[0] and vx < 0: vx = 0
		if leftestCol[0]: vx = 0.5
		if topCol[0] and vy < 0: vy = 0
		if toppestCol[0]: vy = 0.5
		if bottomCol[0] and vy > 0: vy = 0
		if bottomestCol[0]: vy = -0.5

		display.fill((255, 255, 255))
		mainSurf.blit(bg, (0, 0))

		if enableShadow:
			shadowSurf.fill((16, 16, 16))
			shadowSurf.blit(shad, (px - 16*5, py - 16*5))

		updateBlocksBuffer(tiles, dimension, tick)
		mainSurf.blit(blocksBuffer, (0, 0))

		mainSurf.blit(shad, (px, py + 8), special_flags=pg.BLEND_RGBA_MULT)

		#display.blit(glow, (px - 32, py - 32))
		display.blit(mainSurf, (0, 0))
		display.blit(anim.sprite("playAr"), (px, py - 16))
		if not debug: display.blit(sh[dimension], (0, 0))

		if st >= 0:
			pg.draw.rect(display, (0, 0, 0), pg.Rect(0, 0, 960, int(((st / 200) ** 2) * 320)))
			pg.draw.rect(display, (0, 0, 0), pg.Rect(0, 640 -int(((st / 200) ** 2) * 320), 960, int(((st / 200) ** 2) * 320)))
			st -= 5

		if debug:
			for i in colliderList[dimension]:
				color = (120, 240, 112)
				if i.kill: color = (223, 36, 36)
				pg.draw.rect(display, color, i, 1)
			for i in range(len(hitboxes)):
				color = (240, 60, 200)
				if cols[i][0]: color = (90, 240, 200)
				pg.draw.rect(display, color, hitboxes[i], 1)

		pg.display.update()

		px += vx
		py += vy

		vx *= 0.8

		if int(time() * 2) % 2:
			if retrigger:
				print(frame)
				frame = 0
			retrigger = False
		else:
			retrigger = True

		if coyote > 0: coyote -= 1

		frame += 1
		tickF += deltaTime
		tick = int(tickF)
		preGameTime = gameTime

mainMenu(display)

pg.mixer.music.fadeout(300)
pg.mixer.music.unload()

for i in range(211):
	pg.event.get()
	pg.draw.rect(display, (0, 0, 0), pg.Rect(0, 0, 960, int(((i / 200) ** 2) * 320)))
	pg.draw.rect(display, (0, 0, 0), pg.Rect(0, 640 -int(((i / 200) ** 2) * 320), 960, int(((i / 200) ** 2) * 320)))
	pg.display.update()
	pg.time.delay(1)

pg.quit()