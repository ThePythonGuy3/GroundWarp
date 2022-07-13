pg = None

class collider:
	def __init__(self, block, x, y, kill, size = 16, impulse = 0):
		self.block = block
		self.rect = pg.Rect(x * 16, y * 16, size, size)
		self.kill = kill
		self.impulse = impulse

def rectCollide(colliderList, rect, ignore = False):
	kill = False
	collide = False
	impulse = 0
	impulseCol = None
	impulseId = 0
	stroboro = None
	for i in colliderList:
		if rect.colliderect(i.rect):
			if ignore and (i.kill or i.impulse != 0 or i.block.strobery): continue
			collide = True
			if i.kill: kill = True
			if i.impulse != 0:
				impulse = i.impulse
				impulseCol = i.block
				impulseId = id(i)
			if i.block.strobery:
				stroboro = i
	return [collide, kill, impulse, impulseCol, impulseId, stroboro]

