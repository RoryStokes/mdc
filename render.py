import pygame, os
from pygame.locals import *

class Renderer:
	def __init__(self,window,map_obstructions,unitManager):
		self.window = window
		self.anchor_x = 16
		self.anchor_y = 16
		self.scale = 40
		self.windowSize = (0,0)
		self.map_obstructions = map_obstructions
		self.unitManager = unitManager
		self.scrollSpeed = 1
		
	def update(self):
		#Draw background
		self.window.fill(pygame.Color(255,255,255))

		#Draw map tiles
		for poly in self.map_obstructions:
			tempPoly = []
			above = below = left = right = True
			for node in poly:
				x,y = self.toScreenCoord(node)
				tempPoly.append((x,y))

				above = above and y < 0
				below = below and y > self.windowSize[1]
				left  = left  and x < 0
				right = right and x > self.windowSize[0]
			if not (above or below or left or right):
				pygame.draw.polygon(self.window, pygame.Color(0,0,0), tempPoly)

			for unit in self.unitManager.units:
				x,y = self.toScreenCoord((unit.x,unit.y))
				radius = int(self.scale*unit.radius)
				if x > -radius and x < self.windowSize[0]+radius and y > -radius and y < self.windowSize[1]+radius:
					baseColour = pygame.Color(80,80,80)
					if unit.good:
						teamColour = pygame.Color(0,255,0)
					else:
						teamColour = pygame.Color(255,0,0)
					if unit.type == 0:
						pygame.draw.circle(self.window, baseColour, (x,y), radius)
						if radius > 5:
							pygame.draw.circle(self.window, teamColour, (x,y), radius-5)
					elif unit.type == 1:
						pygame.draw.circle(self.window, teamColour, (x,y), radius)
					elif unit.type == 2:
						pygame.draw.circle(self.window, baseColour, (x,y), radius)
						if radius > 5:
							pygame.draw.circle(self.window, teamColour, (x,y), radius-5)
							if radius > 10:
								pygame.draw.circle(self.window, baseColour, (x,y), radius-10)



	def toGlobalCoord(self,(x,y)):
		dx = (x - self.windowSize[0]/2.0) * (1.0/self.scale)
		dy = (y - self.windowSize[1]/2.0) * (1.0/self.scale)
		return (dx+self.anchor_x,dy+self.anchor_y)

	def toScreenCoord(self,(x,y)):
		dx = self.scale*(x-self.anchor_x)
		dy = self.scale*(y-self.anchor_y)

		return (int(dx+self.windowSize[0]/2), int(dy+self.windowSize[1]/2))

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
