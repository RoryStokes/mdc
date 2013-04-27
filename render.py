import pygame, os
from pygame.locals import *

class Renderer:
	def __init__(self,window,map_obstructions,units):
		self.window = window
		self.units = units
		self.map_obstructions = []
		for poly in map_obstructions:
			temp =[]
			for x,y in poly:
				temp.append((20*x,20*y))
			self.map_obstructions.append(temp)
		
	def update(self):
		#Draw background
		self.window.fill(pygame.Color(255,255,255))
		
		#Draw map tiles
		for poly in self.map_obstructions:
			pygame.draw.polygon(self.window, pygame.Color(0,0,0), poly)

		#Draw units
		for unit in self.units:
			pygame.draw.circle(self.window, pygame.Color(255,0,0), unit.pos(), 2)
