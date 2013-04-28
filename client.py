from twisted.internet import protocol, reactor
from twisted.protocols import amp
from sys import stdout
from commands import MoveTo, FollowPath
import datetime

class NetworkHandler(amp.AMP):
    def __init__(self, manager):
        self.manager = manager

    def connectionMade(self):
        self.synchronise()
        self.callRemote(MoveTo, entity=1, x=0.5, y=0.7)

    def synchronise(self):
        start = datetime.now()
        def onDone(result):
            now = datetime.now()
            ping = now - start
            self.manager.offset = result['time'] + (ping // 2) - now
        self.callRemote(Synchronise).addCallback(onDone)

    def newTurn(self, turn, end):
        if self.manager.turn != turn:
            stdout.write("Lagging\n")
            self.manager.turn = turn
        self.manager.turnEnd = end
        return {}
    NewTurn.responder(newTurn)

    def path(self, entity, path):
        for point in path:
            stdout.write(str(point['x'])+", "+str(point['y'])+"\n")
        stdout.flush()
        return {}
    FollowPath.responder(path)

class NetworkManager(protocol.ReconnectingClientFactory):
    def __init__(self):
        self.turn = 0
        self.time = datetime.now()
        self.offset = datetime.timedelta(0)
        self.timeout = datetime.timedelta(0,1)

    def update(self):
        newTime = datetime.now()
        dt = newTime - self.time
        self.time = newTime
        

    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        print 'Resetting reconnection delay'
        self.resetDelay()
        return NetworkHandler(self)

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                                  reason)

host = "127.0.0.1"
port = 1234
network = NetworkManager()
reactor.connectTCP(host, port, manager)
reactor.run()
