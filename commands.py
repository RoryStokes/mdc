from twisted.protocols import amp

class Ready(amp.Command):
       arguments = []
       response = [('time', amp.DateTime())]

class StartGame(amp.Command):
       arguments = [('time', amp.DateTime())]
       response = []

class Done(amp.Command):
       arguments = [('turn', amp.Integer()),
                    ('ping', amp.Float())]
       response = [('success', amp.Boolean())]

class Order(amp.Command):
       arguments = [('turn', amp.Integer()),
                    ('x', amp.Float()),
                    ('y', amp.Float())]
       response = [('success', amp.Boolean())]
