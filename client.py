from twisted.internet import protocol, reactor
from twisted.protocols import amp
from sys import stdout
from commands import MoveTo, FollowPath

class NetworkHandler(amp.AMP):
    def connectionMade(self):
        self.callRemote(MoveTo, entity=1, x=0.5, y=0.7)

    def path(self, entity, path):
        for point in path:
            stdout.write(str(point['x'])+", "+str(point['y'])+"\n")
        stdout.flush()
        return {}
    FollowPath.responder(path)

class NetworkFactory(protocol.ReconnectingClientFactory):
    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        print 'Resetting reconnection delay'
        self.resetDelay()
        return NetworkHandler()

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                                  reason)

host = "127.0.0.1"
port = 1234
reactor.connectTCP(host, port, NetworkFactory())
reactor.run()
