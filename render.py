import pygame, os
from pygame.locals import *

class Renderer:
	def __init__(self,window,event,map_obstructions):
		self.window = window
		self.event  = event
		self.map_obstructions = []
		for poly in map_obstructions:
			temp =[]
			for x,y in poly:
				temp.append((20*x,20*y))
			self.map_obstructions.append(temp)
		event.register("update", self.update)
		
	def update(self):
		#Draw background
		self.window.fill(pygame.Color(255,255,255))
		
		#Draw map tiles
		for poly in self.map_obstructions:
			pygame.draw.polygon(self.window, pygame.Color(0,0,0), poly)
