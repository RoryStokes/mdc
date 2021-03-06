from node import Node
import math, entity


class Entity(object):
  def __init__(self, x, y, health):
    super(Entity, self).__init__()

    self.health = health
    self.alive = True
    self.x, self.y = float(x), float(y)

  def damage(self, damageAmount):
    self.health -= damageAmount

    if self.health <= 0:
      self.alive = False

  def visibleNodes(self, board):
        currentNode = Node(self.x, self.y)
        
        return board.get_visible_set(currentNode)

  def canSee(self, board, node):
      nodeList = visibleNodes(board)

      return node in nodeList

  def pos(self):
      return (self.x, self.y)

class Unit(entity.Entity):
    def __init__(self, pos,good, unit_type, board):
        super(Unit, self).__init__(pos.x, pos.y, 100)

        self.target = pos
        self.path = []
        self.speed = 0.08
        self.dir = 0
        self.radius = 0.5
        self.board = board#.get_expanded(-0.5)
        self.type = unit_type
        self.good = good
        self.damage = 0
        if self.type == 0:
            self.speed = 0.1
        if self.type == 2:
            self.radius = 4
        self.maxRad = self.radius
        self.growRate = self.radius / 300

        #TYPES:
        # 0 - player
        # 1 - creep
        # 2 - tower
        # 3 - hero

    def pathTo(self, moveToPos):
        currentNode = Node(self.x, self.y)
        targetNode = Node(moveToPos[0], moveToPos[1])

        self.setPath( self.board.get_shortest_path(currentNode, targetNode) )

    def setPath(self,path):
        if path != None:
            print path
            self.path = path
            self.target = self.path.pop(0)

    def getRadius(self):
        return self.radius

    def takeDamage(self,damage):
        self.radius -= damage;
        if self.type == 0:
            self.damage += damage
            while self.damage > 0.05:
                self.damage -= 0.05
                self.maxRad += 0.005
        if self.radius < 0.1:
            self.radius = 0

    def update(self):
        reached = True

        dx = self.target.x - self.x
        dy = self.target.y - self.y

        ds = math.hypot(dx, dy)

        if ds > self.speed:
            self.x += self.speed * dx / ds
            self.y += self.speed * dy / ds
        else:
            self.x = self.target.x
            self.y = self.target.y
            if len(self.path) > 0:
                print "POP"
                self.target = self.path.pop(0)

        if self.type == 0:
            if self.radius + self.growRate < self.maxRad:
                self.radius += self.growRate
            else:
                self.radius = self.maxRad
