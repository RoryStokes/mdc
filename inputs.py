from pygame.locals import *

class InputManager:
  def __init__(self, event, renderer):
    self.event = event
    self.renderer = renderer

  def registerClick(self, pos, button, down):
    x,y = self.renderer.toGlobalCoord(pos)
    
    if down and button == 3:
      self.event.notify("leftClick",x,y)
    elif down and button == 1:
      self.event.notify("rightClick",x,y)

  def registerKey(self, key, down):
    pass