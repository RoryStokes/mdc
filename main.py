import geometry
import mapping
from node import Node
import unittest
import render, event, inputs, collision
import pygame, sys
from unit import Unit
from pygame.locals import *

map_obstructions = [
[(4, 10), (10, 4), (10, 10)],       #top left inner
[(22,4), (28,10), (22,10)],         #top right inner
[(4,22), (10,22), (10,28)],         #bottom left inner
[(22,22), (28,22), (22,28)],        #bottom right inner
[(0,26),(6,32),(0,32)],             #bottom left outer
[(26,0),(32,0),(32,6)],             #top right outer
[(4,13),(28,13),(28,14),(4,14)],    #river top boundary
[(4,18),(28,18),(28,19),(4,19)]]    #river bot boundary

map_board = mapping.Board()

for poly in map_obstructions:
    map_board.add( geometry.Polygon(*poly, ccw=False) )

pygame.init()
clock         = pygame.time.Clock()
event_manager = event.Event()
window        = pygame.display.set_mode((640,400),pygame.RESIZABLE)
pygame.display.set_caption("MDC")

units = []
def addUnit(unit):
    event_manager.register("update", unit.update)
    units.append(unit)
def addPlayer(pos,good):
    player = Unit(pos,good,0,map_board)
    addUnit(player)
    event_manager.register("rightClick", player.pathTo)

creepSpawns  = [Node(2,2),Node(30,30)]
bottomCorner = [Node(2,24),Node(8,30)]
topCorner    = [Node(24,2),Node(30,8)]


def addCreep(good,top):
    if top:
        corner = topCorner
    else:
        corner = bottomCorner

    if good:
        creep = Unit(creepSpawns[0],True,1,map_board)
        creep.setPath(corner + [creepSpawns[1]])
    else:
        creep = Unit(creepSpawns[1],False,1,map_board)
        creep.setPath(corner[::-1] + [creepSpawns[0]]) 
    addUnit(creep)

addPlayer(Node(5,5),True)
addPlayer(Node(27,5),False)

for good in (True,False):
    for top in (True,False):
        addCreep(good,top)

renderer         = render.Renderer(window, map_obstructions, units)
inputManager     = inputs.InputManager(event_manager, renderer)
collisionManager = collision.CollisionManager(event_manager, units)
renderer.setWindowSize((640,400))
event_manager.register("keyDown", renderer.moveAnchor)
event_manager.register("update", collisionManager.update)

while True:
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == VIDEORESIZE:
            pygame.display.set_mode((e.size),pygame.RESIZABLE)
            renderer.setWindowSize(e.size)
        elif e.type == MOUSEBUTTONDOWN:
            inputManager.registerClick(e.pos, e.button, True)
        elif e.type == MOUSEBUTTONUP:
            inputManager.registerClick(e.pos, e.button, False)
        elif e.type == KEYDOWN:
            inputManager.registerKey(e.key, True)
        elif e.type == KEYUP:
            inputManager.registerKey(e.key, False)

    event_manager.notify("update")
    event_manager.update()
    renderer.update()
    pygame.display.update()

    clock.tick(30)
