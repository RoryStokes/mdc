from twisted.internet import protocol, reactor
from twisted.protocols import amp
from commands import Ready, StartGame, Order, Done, SendConns
import datetime

class SpectatorHandler(amp.AMP):
    pass

class NetworkHandler(amp.AMP):
    def __init__(self, manager):
        self.manager = manager
        self.done    = True
        self.port    = 8888

    def ready(self):
        self.manager.ready[self] = True
        return {'time': datetime.datetime.now()}
    Ready.responder(ready)

    def start(self, time, turnLength):
        self.manager.start[self] = (time, datetime.timedelta(0, turnLength))
        return {}
    StartGame.responder(start)

    def order(self, turn, x, y):
        if turn <= self.manager.turn:
            return {'success': False}
        self.manager.queueOrder(turn, self, x, y)
        return {'success': True}
    Order.responder(order)

    def done(self, turn, ping):
        if turn != self.manager.turn - 1 and turn != self.manager.turn:
            return {'success': False}
        if self.manager.done[turn] == None:
            self.manager.done[turn] = {}
        self.manager.done[turn][self] = datetime.timedelta(0, ping)
        self.manager.checkDone()
        return {'success': True}
    Done.responder(done)

    def connectionMade(self):
        connList = [{'host':str(conn.host),'port':int(client.port)} for conn, client in self.manager.clients.items() if client is not self]
        self.callRemote(SendConns, port=self.manager.port, conns=connList)

    def getConns(self, conns, port):
        self.port = port
        for conn in conns:
            if (conn['host'],conn['port']) not in [(str(c.host),int(client.port)) for c, client in self.manager.clients.items() if client is not self]:
                reactor.connectTCP(conn['host'],conn['port'],self.manager)
        return {}
    SendConns.responder(getConns)

class NetworkManager(protocol.ClientFactory):
    def __init__(self, port):
        self.port = port
        self.clients = {}
        self.turn = 0
        self.cTurn = self.turn + 3
        self.ready = {}
        self.readyPing = {}
        self.offset = {}
        self.done = {}
        self.orders = {}
        self.ping = {}
        self.readyTime = None
        self.running = False
        self.turnLength = datetime.timedelta(0,0,50)
        self.timeout = None
        self.turnEnd = None

    def ready(self):
        if self not in self.ready:
            self.ready[self] = True
            self.readyTime = datetime.datetime.now()
            for client in self.clients.itervalues():
                def callback():
                    self.readyPing[client] = datetime.datetime.now() - self.readyTime
                    self.offset[client] = result['time'] - self.readyTime - (datetime.datetime.now() - self.readyTime)//2
                client.callRemote(Ready).addCallback(callback)
            self.readying()

    def endTurn(self):
        self.cTurn += 1
        self.ping[self.cTurn-1] = datetime.timedelta(0,0,50)
        for client in self.clients.itervalues():
            client.callRemote(Done, turn=self.cTurn-1, ping=self.ping[self.cTurn-1].to_seconds())
        self.timeout = reactor.callLater(1, self.onTimeout)
        self.checkDone()

    def beginTurn(self):
        self.running = True
        if turn in self.done:
            del self.done[turn]
        self.turn += 1
        if turn in self.orders:
            for o in self.orders:
                self.doOrder(*o)
            del self.orders[turn]
        reactor.callLater(self.turnLength, self.endTurn)

    def checkDone(self):
        if self.turn-1 in self.done and len(self.done[self.turn-1]) == len(self.clients):
            latency = max(max(self.done[self.turn-1].itervalues()), self.ping[self.turn-1])
            self.turnLength = (9*self.turnLength + maxLatency + latency // 10) // 10
            self.turnEnd = datetime.datetime.now() + self.turnLength
            if self.timeout != None:
                self.timeout.stop()
                self.timeout = None
            self.beginTurn()

    def onTimeout(self):
        print("Timeout")

    def sendOrder(self, x, y):
        if self.running:
            for client in self.clients.itervalues():
                client.callRemote(Order, turn=self.cTurn, x=x, y=y)
            self.queueOrder(self.cTurn, x, y)

    def queueOrder(self, turn, client, x, y):
        if self.orders[turn] == None:
            self.orders[turn] = []
        self.orders[turn].push((client, x, y))

    def doOrder(self, client, x, y):
        print("Do order", client, x, y)
    
    def readying(self):
        if len(self.ready) > len(self.clients):
            latency = max(self.readyPing.itervalues())
            now = datetime.datetime.now()
            self.start[self] = (now + 5*latency, latency+latency//10)
            for client in self.clients.itervalues():
                client.callRemote(StartGame, time=now + 5*latency, turnLength=(latency+latency//10).to_seconds()) 
            reactor.callLater(0.1, self.starting)
        else:
            reactor.callLater(0.1, self.readying)

    def starting(self):
        if len(self.start) > len(self.clients):
            self.turnLength = max([x[1] for client,x in self.start.iter()])
            self.turnEnd = max([x[0]-self.offset[client] for client,x in self.start.iter()])
            reactor.callLater(self.turnEnd - datetime.datetime.now(), self.beginTurn)
        else:
            reactor.callLater(0.1, self.starting)

    def buildProtocol(self, addr):
        if len(self.clients) < self.numPlayers:
            newClient = NetworkHandler(self)
            self.clients[addr] = newClient
            if len(self.clients) == self.numPlayers:
                self.ready()
        else:
            newClient = SpectatorClient()
        return newClient
