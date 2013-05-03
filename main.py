import geometry
import mapping
import render, event, inputs, units, network
import pygame, sys
from pygame.locals import *
from twisted.internet import reactor
import zope.interface

clock = None
creepTime     = {-1: 1}
window = None

def init():
	pygame.init()
	clock         = pygame.time.Clock()
	window        = pygame.display.set_mode((640,400),pygame.RESIZABLE)
	pygame.display.set_caption("MDC")

	renderer.window = window

	eventManager.register("windowResize", renderer.setWindowSize)
	eventManager.register("setPan", renderer.setPan)
	eventManager.register("keyDown", renderer.moveAnchor)
	eventManager.register("windowResize", inputManager.setWindowSize)
	eventManager.register("update",inputManager.update)
	eventManager.register("update",unitManager.update)
	eventManager.register("creepAdd", unitManager.spawnWave)
	eventManager.notify("windowResize",(640,400))

def update(n):
	for e in pygame.event.get():
		if e.type == QUIT:
			pygame.quit()
			sys.exit()
		elif e.type == VIDEORESIZE:
			pygame.display.set_mode((e.size),pygame.RESIZABLE)
			eventManager.notify("windowResize", e.size)
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
	for k in creepTime:
		creepTime[k] -= 1
		if creepTime[k] == 0:
			if k == -1:
				eventManager.notify("creepAdd")
				creepTime[-1] = 300
			else:
				unitManager.addPlayer(isGood[k],k)
	if n > 1:
		reactor.callLater(0.03, update, n-1)

host = raw_input("Enter IP to connect to (leave blank to host): ")

if host != "":
	remotePort = raw_input("Enter port to connect to (leave blank to use default - 8888): ")
	if remotePort == "":
		remotePort = 8888
	else:
		remotePort = int(remotePort)

	port = raw_input("Enter port to listen on (leave blank to use default - 8889): ")
	if port == "":
		port = 8889
	else:
		port = int(port)
else:
	port = raw_input("Enter port to listen on (leave blank to use default - 8888): ")
	if port == "":
		port = 8888
	else:
		port = int(port)

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

def respawnPlayer(id):
	 creepTime[id] = 300   

eventManager  = event.Event()
unitManager   = units.UnitManager(eventManager, map_board, respawnPlayer)

renderer      = render.Renderer(None, map_obstructions, unitManager)
inputManager  = inputs.InputManager(eventManager, renderer)

isGood = {}

def addPlayer(good, id):
		unitManager.addPlayer(good, id)
		isGood[id] = good

players = 2
networkManager = network.NetworkManager(players, port, init, update, unitManager.moveOrder, addPlayer)

if host != "":
	reactor.connectTCP(host, remotePort, networkManager)
else:
	networkManager.server = True
reactor.listenTCP(port, networkManager)

eventManager.register("rightClick", networkManager.sendOrder)

unitManager.addAncient(True)
unitManager.addAncient(False)

print "Please wait, connecting to other player..."

reactor.run()
