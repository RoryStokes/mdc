import pygame, os
from pygame.locals import *

class Renderer:
	def __init__(self,window,event,map_obstructions):
		self.window = window
		self.event  = event
		self.anchor = (0,0)
		self.scale = 40
		self.map_obstructions = map_obstructions
		event.register("update", self.update)
		
	def update(self):
		#Draw background
		self.window.fill(pygame.Color(255,255,255))
		
		#Draw map tiles
		for poly in self.map_obstructions:
			tempPoly = []
			onScreen = False
			for x,y in poly:
				x = self.scale*(x-self.anchor[0])
				y = self.scale*(y-self.anchor[1])
				tempPoly.append((x,y))
				if x > 0 and y > 0:
					onScreen = True

			if onScreen:
				pygame.draw.polygon(self.window, pygame.Color(0,0,0), tempPoly)

	def toGlobalCoord((x,y)):
		return (x,y)