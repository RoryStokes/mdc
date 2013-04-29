from entity import Unit
from node import Node
from math import sqrt

class UnitManager:
	def __init__(self,eventManager,map_board):
		self.event = eventManager
		self.units = []
		self.map   = map_board
                
                self.players = {}
                self.event.register("moveOrder", self.moveOrder)

		self.spawnPoints  = [Node(2,2),Node(30,30)]
		self.bottomCorner = [Node(2,24),Node(8,30)]
		self.topCorner    = [Node(24,2),Node(30,8)]

        def moveOrder(self, id, x, y):
                if id in self.players:
                        self.players[id].pathTo((x, y))

	def update(self):
		dead = []
		for unit in self.units:
			if unit.radius < 0.1:
				print "DEAD"
				dead.append(unit)
			else:
				unit.update()

		for i in dead:
			self.units.remove(i)


		unitCount = len(self.units)

		for i in xrange(0,unitCount):
			for j in xrange(i+1,unitCount):
				#for each pair of units
				self.testCollision(self.units[i],self.units[j])

	def testCollision(self,a,b):
		if(a.good != b.good):
			dx = a.x - b.x
			dy = a.y - b.y
			d2 = dx*dx + dy*dy

			r  = (a.getRadius() + b.getRadius())
			r2 = r*r

			if d2<r2:
				print("COLLISION")
				d = sqrt(d2)
				overlap = r - d
				print overlap
				a.takeDamage(overlap/2)
				b.takeDamage(overlap/2)

	def addUnit(self,unit):
		print "added", unit.type, len(self.units)
		self.units.append(unit)

	def addPlayer(self,good,id):
		if good:
			pos=self.spawnPoints[0]
		else:
			pos=self.spawnPoints[1]
		player = Unit(pos,good,0,self.map)
                self.players[id] = player
		self.addUnit(player)

	def addCreep(self,good,top):
		print good, top
		if top:
			corner = self.topCorner
		else:
			corner = self.bottomCorner

		if good:
			creep = Unit(self.spawnPoints[0],True,1,self.map)
			creep.setPath(corner + [self.spawnPoints[1]])
		else:
			creep = Unit(self.spawnPoints[1],False,1,self.map)
			creep.setPath(corner[::-1] + [self.spawnPoints[0]]) 
		self.addUnit(creep)


	def spawnWave(self):
		for good in (True,False):
			for top in (True,False):
				self.addCreep(good,top)
