pg = None

class collider:
	def __init__(self, x, y, kill):
		self.rect = pg.Rect(x * 16, y * 16, 16, 16)
		self.kill = kill

def rectCollide(colliderList, rect):
	output = []
	for i in colliderList:
		if rect.colliderect(i.rect):
			output.append(i)
	return output

