from twisted.internet import protocol, reactor
from twisted.protocols import amp
from commands import Order, Done, SendConns
import datetime

class NetworkHandler(amp.AMP):
    def __init__(self, manager):
        self.manager = manager
        self.done    = True

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
        self.manager.done[turn][self] = ping
        return {'success': True}
    Done.responder(done)

    def connectionMade(self):
        connList = [{'host':str(conn.host),'port':int(conn.port)} for conn, client in self.manager.clients.items() if client is not self]
        print "send", connList
        self.callRemote(SendConns, conns=connList)

    def getConns(self, conns):
        for conn in conns:
            reactor.connectTCP(conn['host'],conn['port'],self.manager)
        return {}
    SendConns.responder(getConns)

class NetworkManager(protocol.ClientFactory):
    def __init__(self):
        self.clients = {}
        self.turn = 0
        self.cTurn = self.turn + 2
        self.time = datetime.datetime.now()
        self.done = {}
        self.orders = {}
        self.ping = {}
        self.turnLength = datetime.timedelta(0,0,50)
        self.timeout = datetime.timedelta(0,1,0)
        self.turnEnd = self.time + self.turnLength

    def endTurn(self):
        self.cTurn += 1
        self.ping[self.cTurn-1] = datetime.timedelta(0,0,50)
        for client in self.clients.itervalues():
            client.callRemote(Done, turn=self.cTurn-1, ping=self.ping[self.cTurn-1])

    def beginTurn(self):
        if turn in self.done:
            del self.done[turn]
        self.turn += 1
        if turn in self.orders:
            for o in self.orders:
                self.doOrder(*o)
            del self.orders[turn]

    def sendOrder(self, x, y):
        for client in self.clients.itervalues():
            client.callRemote(Order, turn=self.cTurn, x=x, y=y)
        self.queueOrder(self.cTurn, x, y)

    def queueOrder(self, turn, client, x, y):
        if self.orders[turn] == None:
            self.orders[turn] = []
        self.orders[turn].push((client, x, y))

    def doOrder(self, client, x, y):
        print("Do order", client, x, y)
    
    def update(self):
        newTime = datetime.now()
        dt = newTime - self.time
        self.time = newTime
        
        if self.turn-1 in self.done and len(self.done[self.turn-1]) == len(self.clients):
            maxLatency = self.ping[self.turn-1]
            for ping in self.done[self.turn-1].itervalues():
                if ping > maxLatency:
                    maxLatency = ping
            self.turnLength = (9*self.turnLength + maxLatency) // 10
            self.turnEnd = self.time + self.turnLength
            self.beginTurn()
    
        if self.time >= self.turnEnd:
            if self.turn < self.cTurn-2:
                print("Timeout")
            elif self.turn == self.cTurn-2:
                self.endTurn()
                self.turnEnd += self.timeout
        
    def buildProtocol(self, addr):
        newClient = NetworkHandler(self)
        self.clients[addr] = newClient
        return newClient
