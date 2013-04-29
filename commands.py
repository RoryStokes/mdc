from twisted.protocols import amp

class Done(amp.Command):
       arguments = [('turn', amp.Integer()),
                    ('ping', amp.Float())]
       response = [('success', amp.Boolean())]

class Order(amp.Command):
       arguments = [('turn', amp.Integer()),
                    ('x', amp.Float()),
                    ('y', amp.Float())]
       response = [('success', amp.Boolean())]

class SendConns(amp.Command):
       arguments = [('conns', amp.AmpList([('host', amp.String()),
                                           ('port',amp.Integer())])),
                    ('port', amp.Integer())]
