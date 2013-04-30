import pygame
from pygame.locals import *

class InputManager:
  def __init__(self, event, renderer):
    self.event = event
    self.renderer = renderer
    self.windowSize = (0,0)
    self.arrowKeys = [False,False,False,False] #up down left right
    self.panSpeed = 0.3
    self.pan = (0,0)


  def update(self):
    xPan, yPan = (0,0)
    x,y = pygame.mouse.get_pos()

    if x < 100:
      xPan = (x-100)/500.0
    elif x > self.windowSize[0]-100:
      xPan = (x-(self.windowSize[0]-100))/500.0

    if y < 100:
      yPan = (y-100)/500.0
    elif y > self.windowSize[1]-100:
      yPan = (y-(self.windowSize[1]-100))/500.0

    if (xPan,yPan) != self.pan:
      self.pan = (xPan,yPan)
      self.event.notify("setPan",(xPan,yPan))


  def setWindowSize(self,size):
    self.windowSize = size

  def registerClick(self, pos, button, down):
    x,y = self.renderer.toGlobalCoord(pos)
    
    if down and button == 1:
      self.event.notify("leftClick", (x,y))
    elif down and button == 3:
      self.event.notify("rightClick", (x,y))

  def registerKey(self, key, down):
    if down:
      if key == K_UP:
        self.arrowKeys[0] = True
      elif key == K_DOWN:
        self.arrowKeys[1] = True
      elif key == K_LEFT:
        self.arrowKeys[2] = True
      elif key == K_RIGHT:
        self.arrowKeys[3] = True
    else:
      if key == K_UP:
        self.arrowKeys[0] = False
      elif key == K_DOWN:
        self.arrowKeys[1] = False
      elif key == K_LEFT:
        self.arrowKeys[2] = False
      elif key == K_RIGHT:
        self.arrowKeys[3] = False

    xPan = yPan = 0

    if self.arrowKeys[0]: yPan -= self.panSpeed
    if self.arrowKeys[1]: yPan += self.panSpeed
    if self.arrowKeys[2]: xPan -= self.panSpeed
    if self.arrowKeys[3]: xPan += self.panSpeed

    self.event.notify("setPan",(xPan,yPan))