import geometry
import mapping
from node import Node
import unittest
import render, event
import pygame
from unit import Unit

map_obstructions = [
[(4, 10), (10, 4), (10, 10)],		#top left inner
[(22,4), (28,10), (22,10)],			#top right inner
[(4,22), (10,22), (10,28)],			#bottom left inner
[(22,22), (28,22), (22,28)],		#bottom right inner
[(0,26),(6,32),(0,32)],				#bottom left outer
[(26,0),(32,0),(32,6)],				#top right outer
[(4,13),(28,13),(28,14),(4,14)],	#river top boundary
[(4,18),(28,18),(28,19),(4,19)]]	#river bot boundary

map_board = mapping.Board()

for poly in map_obstructions:
	map_board.add( geometry.Polygon(*poly, ccw=False) )

pygame.init()
clock   = pygame.time.Clock()
event_manager = event.Event()
window   = pygame.display.set_mode((640,640),pygame.RESIZABLE)
pygame.display.set_caption("MDC")
units = [Unit(5, 5)]
renderer = render.Renderer(window, map_obstructions, units)
event_manager.register("update", renderer.update)

while True:	
	event_manager.notify("update")
	event_manager.update()
	pygame.display.update()
	clock.tick(30)
