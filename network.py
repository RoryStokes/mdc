from twisted.internet import protocol
from twisted.protocols import amp
from commands import Order, Done
import datetime

class NetworkHandler(amp.AMP):
    def __init__(self, manager):
        self.manager = manager
        self.done = True

    def ready(self):
        self.manager.ready[self] = True
        return {'time': datetime.datetime.now()}
    Ready.responder(ready)

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

class NetworkManager(protocol.ClientFactory):
    def __init__(self):
        self.clients = {}
        self.turn = 0
        self.cTurn = self.turn + 3
        self.time = datetime.datetime.now()
        self.ready = {}
        self.offset = {}
        self.done = {}
        self.orders = {}
        self.ping = {}
        self.readyTime = None
        self.running = False
        self.readying = True
        self.starting = True
        self.turnLength = datetime.timedelta(0,0,50)
        self.timeout = datetime.timedelta(0,1,0)
        self.turnEnd = self.time + self.turnLength

    def sendReady(self):
        if self not in self.ready:
            self.ready[self] = datetime.timedelta(0)
            self.readyTime = datetime.datetime.now()
            for client in self.clients.itervalues():
                client.callRemote(Ready).addCallback(
                    lambda result: self.ready[client], self.offset[client] = datetime.now() - self.readyTime, result['time'] - self.readyTime - (datetime.now() - self.readyTime)//2
                )

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
    
    def update(self):
        newTime = datetime.datetime.now()
        dt = newTime - self.time
        self.time = newTime
        
        if not self.running:
            if self.readying:
                if len(self.ready) > len(self.clients):
                    latency = max(self.ready.itervalues())
                    self.start[self] = (self.time + 5*latency, latency+latency//10)
                    for client in self.clients.itervalues():
                        client.callRemote(StartGame, time=self.time + 5*latency, turnLength=latency+latency//10) 
                    self.readying = False
            elif self.starting:
                if len(self.start) > len(self.clients):
                    self.turnLength = max([x[1] for x in self.start])
                    self.turnEnd = max([x[0] for x in self.start])
                    self.starting = False
            elif self.time >= self.turnEnd:
                self.beginTurn()
                self.running = True
        else:
            if self.turn-1 in self.done and len(self.done[self.turn-1]) == len(self.clients):
                latency = max(max(self.done[self.turn-1].itervalues()), self.ping[self.turn-1])
                self.turnLength = (9*self.turnLength + maxLatency + latency // 10) // 10
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
