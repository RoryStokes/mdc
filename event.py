class Event():
  def __init__(self):
    self.handlers = dict()
    self.added =[]
    self.removed = []
    self.events = []

  def register(self, event, handler):
    self.added.append((event, handler))
    return self

  def deregister(self, event, handler):
    if event in self.handlers:
      self.removed.append((event, handler))
    else:
      raise ValueError("Event is not registered, so cannot deregister it.")
    return self

  def notify(self, event, *args, **kargs):
    self.events.append((event, args, kargs))
  
  def update(self):
    # add handlers
    for a in self.added:
      if not a[0] in self.handlers:
        self.handlers[a[0]] = set()
      self.handlers[a[0]].add(a[1])
    # clear removed handlers
    for r in self.removed:
      try:
        self.handlers[r[0]].remove(r[1])
      except:
        raise ValueError("Handler is not handling this event, so cannot deregister it.")
    self.removed = []
    # Send events
    for e in self.events:
      if e[0] in self.handlers:
        for handler in self.handlers[e[0]]:
          handler(*e[1], **e[2])
    self.events = []

# command received from server
#   cmd_rcv(str cmd)
