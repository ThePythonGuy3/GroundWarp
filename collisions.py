pg = None

class collider:
	def __init__(self, x, y, kill, size = 16):
		self.rect = pg.Rect(x * 16, y * 16, size, size)
		self.kill = kill

def rectCollide(colliderList, rect, ignore = False):
	kill = False
	collide = False
	for i in colliderList:
		if rect.colliderect(i.rect):
			if ignore and i.kill: continue
			
			collide = True
			if i.kill: kill = True
	return [collide, kill]

