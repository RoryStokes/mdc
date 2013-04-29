import geometry
import mapping
import render, event, inputs, units, network
import pygame, sys
from pygame.locals import *
from twisted.internet import reactor

host = raw_input("Enter IP to connect to (leave blank to host): ")

if host != "":
        remotePort = raw_input("Enter port to connect to (leave blank to use default - 8888): ")
        if remotePort == "":
                remotePort = 8888
        else:
                remotePort = int(remotePort)

port = raw_input("Enter port to listen on (leave blank to use default - 8888): ")
if port == "":
	port = 8888
else:
	port = int(port)

networkManager = network.NetworkManager(port)

if host != "":
	reactor.connectTCP(host, remotePort, networkManager)
reactor.listenTCP(port, networkManager)
reactor.run()

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
eventManager  = event.Event()
window        = pygame.display.set_mode((640,400),pygame.RESIZABLE)
pygame.display.set_caption("MDC")


unitManager      = units.UnitManager(eventManager, map_board)
renderer         = render.Renderer(window, map_obstructions, unitManager)
inputManager     = inputs.InputManager(eventManager, renderer)
renderer.setWindowSize((640,400))
eventManager.register("keyDown", renderer.moveAnchor)
eventManager.register("update",unitManager.update)
eventManager.register("creepAdd", unitManager.spawnWave)


unitManager.addPlayer(True)
unitManager.addPlayer(False)

eventManager.notify("creepAdd")

while False: #True:
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

	eventManager.notify("update")
	eventManager.update()
	renderer.update()
	pygame.display.update()

	clock.tick(30)
