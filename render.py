import pygame, os
from pygame.locals import *

class Renderer:
	def __init__(self,window,map_obstructions,units):
		self.window = window
		self.anchor = (16,16)
		self.scale = 40
		self.windowSize = (0,0)
		self.map_obstructions = map_obstructions
		self.units = units
		
	def update(self):
		#Draw background
		self.window.fill(pygame.Color(255,255,255))

		#Draw map tiles
		for poly in self.map_obstructions:
			tempPoly = []
			onScreen = True
			for x,y in poly:
				x = self.scale*(x-self.anchor[0]) + self.windowSize[0]/2
				y = self.scale*(y-self.anchor[1]) + self.windowSize[1]/2
				tempPoly.append((x,y))
				if x > 0 and x < self.windowSize[0] and y > 0 and y < self.windowSize[1]:
					onScreen = True
			if onScreen:
				pygame.draw.polygon(self.window, pygame.Color(0,0,0), tempPoly)

	def toGlobalCoord(self,(x,y)):
		x_disp = (x - self.windowSize[0]/2) * (32/self.windowSize[0])
		y_disp = (y - self.windowSize[1]/2) * (32/self.windowSize[1])
		return (x_disp+self.anchor[0],y_disp+self.anchor[1])

	def setWindowSize(self,(x,y)):
		self.windowSize = (x,y)