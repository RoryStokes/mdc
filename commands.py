from twisted.protocols import amp

class MoveTo(amp.Command):
       arguments = [('entity', amp.Integer()),
                    ('x', amp.Float()),
                    ('y', amp.Float())]
       response = []

class FollowPath(amp.Command):
       arguments = [('entity', amp.Integer()),
                    ('path', amp.AmpList([('x', amp.Float()),
                                          ('y', amp.Float())]))]
       response = []
