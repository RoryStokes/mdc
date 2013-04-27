from twisted.internet import protocol, reactor
from twisted.protocols import amp
from sys import stdout
from commands import MoveTo, FollowPath

class ClientHandler(amp.AMP):
    def __init__(self, clients):
        self.clients = clients

    def move(self, entity, x, y):
        p = [{'x': x, 'y': y}]
        stdout.write(str(x)+", "+str(y)+"\n")
        stdout.flush()
        for addr in self.clients:
            client = self.clients[addr]
            client.callRemote(FollowPath, entity=entity, path=p)
        return {}
    MoveTo.responder(move)

class ClientFactory(protocol.Factory):
    def __init__(self):
        self.clients = {}
    
    def buildProtocol(self, addr):
        newClient = ClientHandler(self.clients)
        self.clients[addr] = newClient
        return newClient

reactor.listenTCP(1234, ClientFactory())
reactor.run()
