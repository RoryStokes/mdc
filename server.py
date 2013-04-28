from twisted.internet import protocol, reactor
from twisted.protocols import amp
from sys import stdout
from commands import MoveTo, FollowPath, NewTurn
import datetime

class NetworkHandler(amp.AMP):
    def __init__(self, manager):
        self.manager = manager
        self.latency = datetime.timedelta(0,0,50)
        self.done = true

    def update(self):
        self.done = false
        def onDone(result):
            self.latency = dateTime.now() - self.manager.turnStart
            self.done = true
        client.callRemote(NewTurn,
                          turn=self.manager.turn,
                          end=self.manager.turnEnd.total_seconds()).addCallback(onDone)

    def move(self, entity, x, y):
        p = [{'x': x, 'y': y}]
        stdout.write(str(x)+", "+str(y)+"\n")
        stdout.flush()
        for client in self.manager.clients.itervalues():
            client.callRemote(FollowPath, entity=entity, path=p)
        return {}
    MoveTo.responder(move)

class NetworkManager(protocol.Factory):
    def __init__(self):
        self.clients = {}
        self.turn = 0
        self.time = datetime.now()
        self.turnLength = datetime.timedelta(0,0,50)
        self.turnStart = self.time
        self.turnEnd = self.time + self.turnLength
    
    def update(self):
        newTime = datetime.now()
        dt = newTime - self.time
        self.time = newTime
        if self.time - self.turnStart >= self.turnLength:
            self.turnStart = self.time
            maxLatency = datetime.timedelta(0)
            for client in self.clients.itervalues():
                if ! client.done:
                    stdout.write("Lagging\n")
                    stdout.flush()
                else:
                    if client.latency > maxLatency:
                        maxLatency = client.latency
                    client.update()
            self.turnLength = (9*self.turnLength + maxLatency) // 10
            self.turn = self.turn + 1
    
    def buildProtocol(self, addr):
        newClient = NetworkHandler(self)
        self.clients[addr] = newClient
        return newClient

manager = NetworkManager()

reactor.listenTCP(1234, manager)
reactor.run()
