from twisted.internet import protocol, reactor
from twisted.protocols import amp
from commands import Ready, StartGame, Order, Done, SendConns
import datetime

class UTC(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(0)
    
    def dst(self, dt):
        return datetime.timedelta(0)
    
    def tzname(self, dt):
        return "UTC"

class SpectatorHandler(amp.AMP):
    pass

class NetworkHandler(amp.AMP):
    def __init__(self, manager):
        self.manager = manager
        self.port    = 8888

    def ready(self):
        self.manager.ready[self] = True
        self.manager.readying()
        return {'time': datetime.datetime.now(UTC())}
    Ready.responder(ready)

    def start(self, ping, time, turnLength):
        self.manager.start[self] = (time, datetime.timedelta(0, turnLength))
        for turn in [0,1,2]:
            if turn not in self.manager.done:
                self.manager.done[turn] = {}
            self.manager.done[turn][self] = datetime.timedelta(0, ping)
        self.manager.starting()
        return {}
    StartGame.responder(start)

    def order(self, turn, x, y):
        if turn <= self.manager.turn:
            return {'success': False}
        self.manager.queueOrder(turn, self, x, y)
        return {'success': True}
    Order.responder(order)

    def done(self, turn, ping):
        if turn not in self.manager.done:
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
    def __init__(self, numPlayers, port, update, doOrder):
        self.numPlayers = numPlayers
        self.port = port
        self.doOrder = doOrder
        self.clients = {}
        self.ids = {self: 0}
        self.turn = 0
        self.cTurn = self.turn + 3
        self.ready = {}
        self.readyPing = {}
        self.offset = {}
        self.done = {}
        self.orders = {}
        self.ping = {}
        self.start = {}
        self.readyTime = None
        self.running = False
        self.waiting = False
        self.turnLength = datetime.timedelta(0,0,0,50)
        self.timeout = None
        self.turnEnd = None
        self.mainLoop = update

    def setReady(self):
        if self not in self.ready:
            self.ready[self] = True
            self.readyTime = datetime.datetime.now(UTC())
            for client in self.clients.itervalues():
                def callback(result):
                    self.readyPing[client] = datetime.datetime.now(UTC()) - self.readyTime
                    self.offset[client] = result['time'] - self.readyTime - (datetime.datetime.now(UTC()) - self.readyTime)//2
                    self.readying()
                client.callRemote(Ready).addCallback(callback)
            self.readying()

    def endTurn(self):
        #print "end", self.cTurn
        self.cTurn += 1
        self.ping[self.cTurn-1] = datetime.timedelta(0,0,0,50)
        for client in self.clients.itervalues():
            client.callRemote(Done, turn=self.cTurn-1, ping=self.ping[self.cTurn-1].total_seconds())
        self.timeout = reactor.callLater(1, self.onTimeout)
        self.waiting = True
        self.checkDone()

    def beginTurn(self):
        self.running = True
        if self.turn in self.done:
            del self.done[self.turn]
        self.turn += 1
        #print "begin", self.turn
        if self.turn in self.orders:
            for o in self.orders[self.turn]:
                self.doOrder(self.ids[o[0]], o[1], o[2])
            del self.orders[self.turn]
        self.mainLoop(1)
        reactor.callLater(self.turnLength.total_seconds(), self.endTurn)

    def checkDone(self):
        if self.waiting and self.turn+1 in self.done and self.turn+1 in self.ping and len(self.done[self.turn+1]) == len(self.clients):
            self.waiting = False
            latency = max(max(self.done[self.turn+1].itervalues()), self.ping[self.turn+1])
            self.turnLength = max((9*self.turnLength + latency + latency // 10) // 10, datetime.timedelta(0,0,0,30))
            self.turnEnd = datetime.datetime.now(UTC()) + self.turnLength
            if self.timeout != None:
                self.timeout.cancel()
                self.timeout = None
            self.beginTurn()

    def onTimeout(self):
        print("Timeout")

    def sendOrder(self, (x, y)):
        if self.running:
            for client in self.clients.itervalues():
                client.callRemote(Order, turn=self.cTurn, x=x, y=y)
            self.queueOrder(self.cTurn, self, x, y)

    def queueOrder(self, turn, client, x, y):
        if turn not in self.orders:
            self.orders[turn] = []
        self.orders[turn].append((client, x, y))
    
    def readying(self):
        if not self.running and len(self.ready) > len(self.clients) and len(self.readyPing) == len(self.clients):
            latency = max(self.readyPing.itervalues())
            now = datetime.datetime.now(UTC())
            self.start[self] = (now + 5*latency, max(latency+latency//10,datetime.timedelta(0,0,0,30)))
            self.offset[self] = datetime.timedelta(0)
            for turn in [0,1,2]:
                self.ping[turn] = datetime.timedelta(0,0,0,50)
            for client in self.clients.itervalues():
                client.callRemote(StartGame, ping=latency.total_seconds(), time=now + 5*latency, turnLength=max(latency+latency//10,datetime.timedelta(0,0,0,30)).total_seconds()) 
            self.starting()

    def starting(self):
        if not self.running and len(self.start) > len(self.clients):
            self.turnLength = max([x[1] for client,x in self.start.iteritems()])
            self.turnEnd = max([x[0]-self.offset[client] for client,x in self.start.iteritems()])
            reactor.callLater((self.turnEnd - datetime.datetime.now(UTC())).total_seconds(), self.beginTurn)

    def buildProtocol(self, addr):
        newClient = None
        if len(self.clients) + 1 < self.numPlayers:
            newClient = NetworkHandler(self)
            self.clients[addr] = newClient
            self.ids[newClient] = len(self.clients)
            if len(self.clients) + 1 == self.numPlayers:
                reactor.callLater(0,self.setReady)
        else:
            newClient = SpectatorClient()
        return newClient
