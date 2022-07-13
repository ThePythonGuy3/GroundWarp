import pygame as pg
from math import *
from time import *
from random import *
from datetime import datetime
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
cock = pg.time.Clock()
display = pg.display.set_mode((960, 640))
pg.display.set_caption("GroundWarp")
pg.display.set_icon(anim.sprite("icon"))

class updater:
	def __init__(self, run, typ):
		self.run = run
		self.typ = typ

class block:
	def __init__(self, animator, kill = False, half = False, spikeGrow = False, impulse = 0):
		self.animator = animator
		self.kill = kill
		self.half = half
		self.spikeGrow = spikeGrow
		self.impulse = impulse

	def copy(self):
		return block(self.animator.copy(), self.kill, self.half, self.spikeGrow, self.impulse)

	def create(self, colliderList, dimension, tilex, tiley, rotation): # Rotation goes in 0-3 format, 0 being upwards and going clockwise
		blocc = self
		if self.impulse != 0:
			blocc = self.copy()
			blocc.animator.currentAnimationFrame = 0

		if self.half:
			for i in range(2):
				if rotation == 0: colliderList[dimension].append(col.collider(blocc, tilex * 2 + i, tiley * 2 + 1, self.kill, impulse = self.impulse))
				if rotation == 1: colliderList[dimension].append(col.collider(blocc, tilex * 2, tiley * 2 + i, self.kill, impulse = self.impulse))
				if rotation == 2: colliderList[dimension].append(col.collider(blocc, tilex * 2 + i, tiley * 2, self.kill, impulse = self.impulse))
				if rotation == 3: colliderList[dimension].append(col.collider(blocc, tilex * 2 + 1, tiley * 2 + i, self.kill, impulse = self.impulse))
		else:
			colliderList[dimension].append(col.collider(blocc, tilex * 2, tiley * 2, self.kill, 32, self.impulse))

		if self.spikeGrow:
			def runner(data):
				if self.animator.currentAnimationFrame == 2:
					if len(data[0][dimension]):
						data[0][dimension].append(col.collider(blocc, tilex * 2, tiley * 2, True))
						data[0][dimension].append(col.collider(blocc, tilex * 2 + 1, tiley * 2, True))
				elif self.animator.currentAnimationFrame == 7:
					while len(data[0][dimension]) > data[1][dimension]:
						data[0][dimension].pop()

			updaters[dimension].append(updater(runner, "spooke"))

		return blocc

#0 is empty
blocks = [
	block(anim.animator(anim.sprite("block"))),
	block(anim.animator(anim.split("block1", 6))),
	block(anim.animator(anim.split("block2", 2), 3)),
	block(anim.animator(anim.sprite("spoike")), True, True),
	block(anim.animator(anim.split("bumper", 4), 15, True), half = True, impulse = -512),
	block(anim.animator(anim.sprite("blockB"))),
	block(anim.animator(anim.sprite("blockB1"))),
	block(anim.animator(anim.split("blockB2", 9), 2, True)),
	block(anim.animator(anim.split("spoikeB", 6), 2), True, True),
	block(anim.animator(anim.split("spoikeB2", 12), 2), False, True, True),
	block(anim.animator(anim.sprite("blockC"))),
	block(anim.animator(anim.sprite("blockC1"))),
	block(anim.animator(anim.sprite("blockC2"))),
	block(anim.animator(anim.sprite("spoikeC")), True, True),
	block(anim.animator(anim.sprite("blockC3")), True, True)
]

playerSprites = [
	anim.animator(anim.sprite("anastasia-stand")), #idle
	anim.animator(anim.splitCustom("anastasia-run", 6, 16, 24), 3), #running
	anim.animator(anim.sprite("anastasia-fall")), #falling
	anim.animator(anim.sprite("anastasia-wall")), #on wall

	anim.animator(anim.sprite("anastasia-stand", True)), #idle
	anim.animator(anim.splitCustom("anastasia-run", 6, 16, 24, True), 3), #running
	anim.animator(anim.sprite("anastasia-fall", True)), #falling
	anim.animator(anim.sprite("anastasia-wall", True)) #on wall
]

playerStates = {
	"idle": 0,
	"running": 1,
	"falling": 2,
	"onWall": 3
}

playerDirections = {
	"right": False,
	"left": True
}

playerDirection = False
playerState = 0

bitmask = anim.split("bitmask", 16)

colliderList = [[], [], []] # Dimensions A, B, C
tiles = [{}, {}, {}]
bitm = [{}, {}, {}]
updaters = [[], [], []]
impulseAnimators = []

mute = [
	False, # Mute music
	False  # Mute sfx
]

pg.font.init()
controlsFont = pg.font.SysFont("twcen", 24)

backgrounds = [anim.sprite("factorybg"), anim.sprite("organicbg"), anim.sprite("forestbg")]
crtag = anim.sprite("creditsTag")

muteButtons = anim.splitCustom("mute-buttons", 3, 24, 24)

playB = anim.sprite("play")
playBH = anim.sprite("play-hover")
playBP = anim.sprite("play-press")

exitB = anim.sprite("exit")
exitBH = anim.sprite("exit-hover")
exitBP = anim.sprite("exit-press")

makeB = anim.sprite("make")
makeBH = anim.sprite("make-hover")
makeBP = anim.sprite("make-press")

pausedS = anim.sprite("paused")

snek = anim.animator(anim.split("gamesnek", 11), 2)
snakeask = anim.sprite("snakeask")
snektext = anim.split("snake", 5)
snekfx = [pg.mixer.Sound("audio/sfx/snek" + str(i + 1) + ".mp3") for i in range(4)]
coll = anim.sprite("collider")
collkill = anim.sprite("colliderkill")

death = pg.mixer.Sound("audio/sfx/death.wav")
select = pg.mixer.Sound("audio/sfx/select.wav")
warpFail = pg.mixer.Sound("audio/sfx/warpFail.wav")

currentLevel = 0

def loadRoom(name):
	global colliderList, updaters, tiles, bitm

	colliderList = [[], [], []]
	updaters = [[], [], []]
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
					else: tiles[r][(x, y)] = blocks[v - 1 + r * 5].create(colliderList, r, x, y, 0)
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

muteButtonsRects = [pg.Rect(0, 640 - 48, 48, 48), pg.Rect(48, 640 - 48, 48, 48)]
exitButtonRect = pg.Rect(960 // 2 - 64, 640 // 2 - 32, 128, 64)

loops = ["audio/music/loop1.mp3", "audio/music/loop2.mp3"]
def mainMenu(display):
	pg.mixer.music.stop()
	pg.mixer.music.unload()
	pg.mixer.music.load("audio/music/menu.mp3")
	pg.mixer.music.play(loops=-1, fade_ms=300)

	logo = anim.sprite("logo")

	running = True

	tickF = tick = 0
	deltaTime = 1

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
		death.set_volume(not mute[1] * 0.5)
		select.set_volume(not mute[1] * 0.5)

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

			if e.type == pg.KEYDOWN:
				if e.key == pg.K_h:
					systime = datetime.now()
					pg.image.save(display, "screenshots/screenshot-" + str(systime.strftime("%Y-%m-%d-%H-%M-%S")) + ".png")

		deltaTime = cock.tick(60)

		msx, msy = pg.mouse.get_pos()

		display.fill((255, 255, 255))

		pg.mixer.music.set_volume(not mute[0])

		if not snakeEnable:
			if len(snakes) < 1000:
				snakes.append((randint(0, 960), randint(0, 640), randint(0, 360), randint(0, 90)))
			for i in snakes:
				snek.updateAnimationFrame(tick + i[3])
				blitRotateCenter(display, snek.animate(), i[2], i[:2:], 1)
			if not (int(time() * 2) % 2):
				timeTrigger = True

			if timeTrigger and int(time() * 2) % 2:
				timeTrigger = False
				choice(snekfx).play()

		for i in range(snakeProg):
			display.blit(snektext[i], (960 - 34 * 5 + i * 32 + 2, 640 - 54))

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
				select.play()
				pbTex = playBP
				running = False
		blitRotateCenter(display, pbTex, (180) * easeang, (playBRect.x, playBRect.y), 1)
		mbTex = makeB
		if makeBRect.collidepoint(msx, msy):
			mbTex = makeBH
			if pressed:
				select.play()
				mbTex = makeBP
				openEditor()
		blitRotateCenter(display, mbTex, (180) * easeang, (makeBRect.x, makeBRect.y), 1)
		ebTex = exitB
		if exitBRect.collidepoint(msx, msy):
			ebTex = exitBH
			if pressed:
				select.play()
				ebTex = exitBP
				running = False
				fullR = True
		blitRotateCenter(display, ebTex, (180) * easeang, (exitBRect.x, exitBRect.y), 1)

		if muteButtonsRects[0].collidepoint(msx, msy):
			if pressed:
				select.play()
				mute[0] = not mute[0]
		blitRotateCenter(display, muteButtons[0], (180) * easeang, (muteButtonsRects[0].x, muteButtonsRects[0].y), 1)
		if mute[0]: blitRotateCenter(display, muteButtons[2], (180) * easeang, (muteButtonsRects[0].x, muteButtonsRects[0].y), 1)

		if muteButtonsRects[1].collidepoint(msx, msy):
			if pressed:
				select.play()
				mute[1] = not mute[1]
		blitRotateCenter(display, muteButtons[1], (180) * easeang, (muteButtonsRects[1].x, muteButtonsRects[1].y), 1)
		if mute[1]: blitRotateCenter(display, muteButtons[2], (180) * easeang, (muteButtonsRects[1].x, muteButtonsRects[1].y), 1)

		if st >= 0:
			pg.draw.rect(display, (0, 0, 0), pg.Rect(0, 0, 960, int(((st / 200) ** 2) * 320)))
			pg.draw.rect(display, (0, 0, 0), pg.Rect(0, 640 -int(((st / 200) ** 2) * 320), 960, int(((st / 200) ** 2) * 320)))
			st -= 5

		pg.display.update()

		tickF += deltaTime / 15
		tick = int(tickF)

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
		if tiles[dimension][i].impulse == 0: tiles[dimension][i].animator.updateAnimationFrame(tick)

		if tiles[dimension][i].animator.animationCheck():
			pg.draw.rect(blocksBuffer, (0, 0, 0, 0), (i[0] * 32, i[1] * 32, 32, 32))
			blocksBuffer.blit(tiles[dimension][i].animator.animate(), (i[0] * 32, i[1] * 32))
			blocksBuffer.blit(bitmask[bitm[dimension][i]], (i[0] * 32, i[1] * 32), special_flags=pg.BLEND_RGBA_MULT)

def updateBackground(dimension):
	global bg
	bg.blit(backgrounds[dimension], (0, 0))

def getPlayerSprite(tick):
	global playerState, playerSprites, playerDirection, playerDirections
	playerSprites[playerState + playerDirection * 4].updateAnimationFrame(tick)

	return playerSprites[playerState + playerDirection * 4].animate()

def mainGame(screen):
	global colliderList, bg, tiles, bitm, blocksBuffer, playerState, playerStates, playerDirection, playerDirections

	screenShakeTime = 0
	screenOffSet = [0, 0]

	pg.mixer.music.fadeout(300)
	pg.mixer.music.load(choice(loops))
	pg.mixer.music.play(loops=-1, fade_ms=300)

	debug = False
	running = True

	tickF = tick = 0
	deltaTime = 1

	roomNames = os.listdir("rooms")

	currentRoom = 0
	px, py, sh = loadRoom(roomNames[0])
	px *= 32
	py *= 32
	ipx = px
	ipy = py

	defaultColliderLen = [len(colliderList[i]) for i in range(3)] # Used for animated spikes

	enableShadow = False

	mainSurf = pg.Surface((960, 640), pg.SRCALPHA, 32)
	shad = anim.sprite("shadow")

	topBox = pg.Rect(0, 0, 20, 6)
	toppestBox = pg.Rect(0, 0, 20, 6)
	bottomBox = pg.Rect(0, 0, 14, 6)
	bottomestBox = pg.Rect(0, 0, 14, 6)
	rightBox = pg.Rect(0, 0, 6, 24)
	rightestBox = pg.Rect(0, 0, 6, 24)
	leftBox = pg.Rect(0, 0, 6, 24)
	leftestBox = pg.Rect(0, 0, 6, 24)
	killBox = pg.Rect(0, 0, 12, 18)

	hitboxes = [topBox, toppestBox, bottomBox, bottomestBox, rightBox, rightestBox, leftBox, leftestBox, killBox]

	dimension = 0
	st = 210

	speed = 32
	a = 16
	vx = 0
	vy = 0

	wpressed = False

	coyote = 0

	frame = 0

	retrigger = True

	previousDimension = 0

	generateBlocksBuffer(tiles, dimension, tick)

	updateBackground(dimension)

	display = pg.Surface((960, 640), pg.SRCALPHA, 32)
	fil = pg.Surface((960, 640))
	paused = False

	impulseQueue = {}

	tickK = True
	ftk = True
	tExit = False
	ended = False
	while running:
		death.set_volume(not mute[1] * 0.5)
		select.set_volume(not mute[1] * 0.5)
		warpFail.set_volume(not mute[1] * 0.7)

		for i in updaters[dimension]:
			if i.typ == "spooke":
				i.run([colliderList, defaultColliderLen])


		previousVx = vx
		previousVy = vy

		if previousDimension != dimension:
			previousDimension = dimension
			generateBlocksBuffer(tiles, dimension, tick)
			updateBackground(dimension)

		warped = 0
		for e in pg.event.get():
			if e.type == pg.QUIT:
				running = False
				tExit = True

			if e.type == pg.KEYDOWN:
				if e.key == pg.K_p:
					debug = not debug

				if e.key == pg.K_ESCAPE:
					paused = True

				if e.key == pg.K_RIGHT:
					dimension += 1
					warped = 1
				if e.key == pg.K_LEFT:
					dimension -= 1
					warped = -1

				if e.key == pg.K_h:
					systime = datetime.now()
					pg.image.save(display, "screenshots/screenshot-" + str(systime.strftime("%Y-%m-%d-%H-%M-%S")) + ".png")

				dimension %= 3

		deltaTime = cock.tick(60) / 1000

		topBox.x = px + 6
		topBox.y = py - 2
		toppestBox.x = px + 6
		toppestBox.y = py - 1
		bottomBox.x = px + 9
		bottomBox.y = py + 27
		bottomestBox.x = px + 9
		bottomestBox.y = py + 26
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

		if bottomCol[0]: coyote = 6

		lp = False
		rp = False
		if pg.key.get_pressed()[pg.K_d]:
			vx += speed * deltaTime
			rp = True
		if pg.key.get_pressed()[pg.K_a]:
			vx -= speed * deltaTime
			lp = True

		if not bottomCol[0]:
			playerState = playerStates["falling"]
		elif int(vx) == 0:
			playerState = playerStates["idle"]
		else:
			playerState = playerStates["running"]
			if vx > 0:
				playerDirection = playerDirections["right"]
			elif vx < 0:
				playerDirection = playerDirections["left"]

		if pg.key.get_pressed()[pg.K_w]:
			if not wpressed and (bottomCol[0] or rightCol[0] or leftCol[0] or coyote > 0):
				if not bottomCol[0] and coyote == 0:
					if rightCol[0]:
						vx = -480 * deltaTime
					else: vx = 480 * deltaTime
				vy = -320

			wpressed = True
		else:
			wpressed = False

		if vy < 512:
			ama = a
			if vy > 0 and ((rightCol[0] and rp) or (leftCol[0] and lp)):
				vy = 32
				ama = 0
				playerState = playerStates["onWall"]
				if rightCol[0]: playerDirection = playerDirections["left"]
				elif leftCol[0]: playerDirection = playerDirections["right"]
			vy += ama

		if rightCol[0] and vx > 0: vx = 0
		if rightestCol[0]: vx = -1
		if leftCol[0] and vx < 0: vx = 0
		if leftestCol[0]: vx = 1
		if topCol[0] and vy < 0: vy = 0
		if toppestCol[0]: vy = 64
		if bottomCol[0] and vy > 0: vy = 0
		if bottomestCol[0]: vy = -64

		if warped != 0:
			if killCol[0]:
				dimension -= warped
				dimension %= 3
				vx = previousVx
				vy = previousVy
				screenShakeTime = 6
				warpFail.play()


		display.fill((255, 255, 255))
		display.blit(bg, (0, 0))
		mainSurf.fill((0, 0, 0, 0))

		if enableShadow:
			shadowSurf.fill((16, 16, 16))
			shadowSurf.blit(shad, (px - 16*5, py - 16*5))

		updateBlocksBuffer(tiles, dimension, tick)
		mainSurf.blit(blocksBuffer, (0, 0))

		mainSurf.blit(shad, (px, py + 8), special_flags=pg.BLEND_RGBA_MULT)

		display.blit(mainSurf, (0, 0))
		display.blit(getPlayerSprite(tick), (px, py - 16))
		if not debug: display.blit(sh[dimension], (0, 0))

		if debug:
			for i in colliderList[dimension]:
				color = (120, 240, 112)
				if i.kill: color = (223, 36, 36)
				pg.draw.rect(display, color, i, 1)
			for i in range(len(hitboxes)):
				color = (240, 60, 200)
				if cols[i][0]: color = (90, 240, 200)
				pg.draw.rect(display, color, hitboxes[i], 1)

		pg.mixer.music.set_volume(not mute[0])

		screenOffSet = [0, 0]
		if screenShakeTime > 0:
			if screenShakeTime % 4 in [0, 1]: screenOffSet[0] = 1.5 * screenShakeTime
			else: screenOffSet[0] = -1.5 * screenShakeTime
			screenShakeTime -= 1

		if killCol[0] and killCol[2] != 0:
			vy = killCol[2]
			impulseQueue[killCol[4]] = [killCol[3], 4]

		for i in impulseQueue.keys():
			if impulseQueue[i][1] < 0:
				continue

			impulseQueue[i][0].animator.updateAnimationFrame(int(impulseQueue[i][1]))
			impulseQueue[i][1] -= 10 * deltaTime

		if (killCol[0] and killCol[1]) or tickK:
			if not tickK:
				death.play()
				vx = 0
				vy = 0
				dimension = 0
				screen.blit(display, screenOffSet)
				for i in range(40):
					pg.event.get()
					cock.tick(60)
					screen.blit(display, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
					pg.display.update()
					pg.time.delay(5)

				pg.draw.rect(screen, (0, 0, 0), (0, 0, 960, 640))

				px = ipx
				py = ipy

			tickK = not tickK

			if not tickK:
				if ftk:
					ftk = False
					vx = 0
					vy = 0
					px = ipx
					pt = ipy

				surff = pg.Surface((960, 640))
				for i in range(39):
					pg.event.get()
					cock.tick(60)
					surff.fill((0, 0, 0))
					pg.draw.circle(surff, (255, 255, 255), (px, py), i * 30)
					screen.blit(display, screenOffSet)
					screen.blit(surff, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
					pg.display.update()
					pg.time.delay(1)

		px += vx
		py += vy * deltaTime

		if px >= 940:
			for i in range(38, -1, -1):
				pg.event.get()
				cock.tick(60)
				surff.fill((0, 0, 0))
				pg.draw.circle(surff, (255, 255, 255), (px, py), i * 30)
				screen.blit(display, screenOffSet)
				screen.blit(surff, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
				pg.display.update()
				pg.time.delay(3)

			currentRoom += 1
			impulseQueue = {}
			if currentRoom == len(roomNames):
				running = False
				ended = True
			else:
				dimension = 0
				px, py, sh = loadRoom(roomNames[currentRoom])
				tickK = True
				px *= 32
				py *= 32
				ipx = px
				ipy = py

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
		tick += 1

		"""if st >= 0:
			pg.draw.rect(display, (0, 0, 0), pg.Rect(0, 0, 960, int(((st / 200) ** 2) * 320)))
			pg.draw.rect(display, (0, 0, 0), pg.Rect(0, 640 -int(((st / 200) ** 2) * 320), 960, int(((st / 200) ** 2) * 320)))
			st -= 5
			px = ipx
			py = ipy"""

		if not tickK: screen.blit(display, screenOffSet)
		if running: pg.display.update()

		if paused:
			inRun = True
			while inRun:
				pressed = False

				for e in pg.event.get():
					if e.type == pg.QUIT:
						inRun = running = False
						tExit = True

					if e.type == pg.KEYDOWN:
						if e.key == pg.K_ESCAPE:
							inRun = False
						if e.key == pg.K_h:
							systime = datetime.now()
							pg.image.save(display, "screenshots/screenshot_" + str(systime.strftime("%Y-%m-%d_%H-%M-%S")) + ".png")

					if e.type == pg.MOUSEBUTTONDOWN:
						if e.button == 1: pressed = True

				msx, msy = pg.mouse.get_pos()

				pg.mixer.music.set_volume((not mute[0]) * 0.2)

				cock.tick(60)

				screen.blit(display, screenOffSet)
				pg.draw.rect(fil, (125, 125, 125), (0, 0, 960, 640))
				screen.blit(fil, (0, 0), special_flags=pg.BLEND_RGBA_MULT)

				if muteButtonsRects[0].collidepoint(msx, msy):
					if pressed:
						select.play()
						mute[0] = not mute[0]
				screen.blit(muteButtons[0], (muteButtonsRects[0].x, muteButtonsRects[0].y))
				if mute[0]: screen.blit(muteButtons[2], (muteButtonsRects[0].x, muteButtonsRects[0].y))

				if muteButtonsRects[1].collidepoint(msx, msy):
					if pressed:
						select.play()
						mute[1] = not mute[1]
				screen.blit(muteButtons[1], (muteButtonsRects[1].x, muteButtonsRects[1].y))
				if mute[1]: screen.blit(muteButtons[2], (muteButtonsRects[1].x, muteButtonsRects[1].y))

				ebTex = exitB
				if exitButtonRect.collidepoint(msx, msy):
					ebTex = exitBH
					if pressed:
						select.play()
						ebTex = exitBP
						inRun = running = False
				screen.blit(ebTex, (exitButtonRect.x, exitButtonRect.y))

				screen.blit(pausedS, (960 // 2 - 96, 50))

				screen.blit(controlsFont.render("ESC = pause/unpause", True, (255, 255, 255)), (16, 16))
				screen.blit(controlsFont.render("W, A, D = movement", True, (255, 255, 255)), (16, 48))

				pg.display.update()

			pg.mixer.music.set_volume(not mute[0])

		paused = False

	if not tExit:
		pg.mixer.music.fadeout(300)

		if not ended:
			for i in range(211):
				pg.event.get()
				pg.draw.rect(display, (0, 0, 0), pg.Rect(0, 0, 960, int(((i / 200) ** 2) * 320)))
				pg.draw.rect(display, (0, 0, 0), pg.Rect(0, 640 -int(((i / 200) ** 2) * 320), 960, int(((i / 200) ** 2) * 320)))
				screen.blit(display, screenOffSet)
				pg.display.update()
				pg.time.delay(5)

		pg.time.delay(1000)
		mainMenu(screen)


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