from math import sqrt 

class CollisionManager:
	def __init__(self,event_manager,units):
		self.units = units
		self.event = event_manager

	def update(self):
		unitCount = len(self.units)
		for i in xrange(0,unitCount):
			for j in xrange(i+1,unitCount):
				self.testCollision(self.units[i],self.units[j])

	def testCollision(self,a,b):
		dx = a.x - b.x
		dy = a.y - b.y
		d2 = dx*dx + dy*dy

		r  = (a.getRadius() + b.getRadius())
		r2 = r*r

		if d2<r2:
			print("COLLISION")
			d = sqrt(d2)
			overlap = r - d
			a.takeDamage(overlap/2)
			b.takeDamage(overlap/2)