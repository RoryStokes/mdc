from pygame.locals import *

class InputManager:
  def __init__(self, event, renderer):
    self.event = event
    self.renderer = renderer

  def registerClick(self, pos, button, down):
    x,y = self.renderer.toGlobalCoord(pos)
    
    if down and button == 1:
      self.event.notify("leftClick", (x,y))
    elif down and button == 3:
      self.event.notify("rightClick", (x,y))

  def registerKey(self, key, down):
    if down:
      if key == K_UP:
        self.event.notify("keyDown", "up")
      elif key == K_DOWN:
        self.event.notify("keyDown", "down")
      elif key == K_LEFT:
        self.event.notify("keyDown", "left")
      elif key == K_RIGHT:
        self.event.notify("keyDown", "right")
    else:
      if key == K_UP:
        self.event.notify("keyUp", "up")
      elif key == K_DOWN:
        self.event.notify("keyUp", "down")
      elif key == K_LEFT:
        self.event.notify("keyUp", "left")
      elif key == K_RIGHT:
        self.event.notify("keyUp", "right")