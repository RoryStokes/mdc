import pygame, os
from pygame.locals import *

class Renderer:
	def __init__(self,window,map_obstructions,units):
		self.window = window
		self.anchor_x = 16
		self.anchor_y = 16
		self.scale = 40
		self.windowSize = (0,0)
		self.map_obstructions = map_obstructions
		self.units = units
		self.scrollSpeed = 1
		
	def update(self):
		#Draw background
		self.window.fill(pygame.Color(255,255,255))

		#Draw map tiles
		for poly in self.map_obstructions:
			tempPoly = []
			onScreen = True
			for x,y in poly:
				x = self.scale*(x-self.anchor_x) + self.windowSize[0]/2
				y = self.scale*(y-self.anchor_y) + self.windowSize[1]/2
				tempPoly.append((x,y))
				if x > 0 and x < self.windowSize[0] and y > 0 and y < self.windowSize[1]:
					onScreen = True
			if onScreen:
				pygame.draw.polygon(self.window, pygame.Color(0,0,0), tempPoly)

			for unit in self.units:
				x = self.scale*(unit.x-self.anchor_x) + self.windowSize[0]/2
				y = self.scale*(unit.y-self.anchor_y) + self.windowSize[1]/2
				if x > 0 and x < self.windowSize[0] and y > 0 and y < self.windowSize[1]:
					pygame.draw.circle(self.window, pygame.Color(255,0,0), (int(x), int(y)), int(self.scale * 0.5))


	def toGlobalCoord(self,(x,y)):
		x_disp = (x - self.windowSize[0]/2) * (32/self.windowSize[0])
		y_disp = (y - self.windowSize[1]/2) * (32/self.windowSize[1])
		return (x_disp+self.anchor_x,y_disp+self.anchor_y)

	def setWindowSize(self,(x,y)):
		self.windowSize = (x,y)

	def moveAnchor(self, dir):
		if dir == "up":
			self.anchor_y -= self.scrollSpeed
		elif dir == "down":
			self.anchor_y += self.scrollSpeed
		elif dir == "left":
			self.anchor_x -= self.scrollSpeed
		elif dir == "right":
			self.anchor_x += self.scrollSpeed