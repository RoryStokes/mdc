from twisted.internet import reactor

import network

manager = network.NetworkManager()

port = 1234
reactor.listenTCP(port, manager)
reactor.run()
