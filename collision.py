from math import sqrt 

class CollisionManager:
	def __init__(self,event_manager,units):
		self.units = units
		self.event = event_manager