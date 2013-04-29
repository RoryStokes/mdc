from twisted.internet import reactor

import network

manager = network.NetworkManager()

host = "127.0.0.1"
port = 1234
reactor.connectTCP(host, port, manager)
reactor.run()

manager.sendOrder(1.0, 1.0)
manager.sendOrder(1.0, 2.0)
manager.sendOrder(2.0, 1.0)
manager.sendOrder(1.0, 1.0)
manager.sendOrder(1.0, 1.0)
