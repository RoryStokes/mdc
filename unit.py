from node import Node
import math, entity

class Unit(entity.Entity):
    def __init__(self, pos,good, unit_type, board):
        super(Unit, self).__init__(pos.x, pos.y, 100)

        self.target = pos
        self.path = []
        self.speed = 0.1
        self.dir = 0
        self.radius = 0.5
        self.board = board#.get_expanded(-0.5)
        self.type = unit_type
        self.good = good

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
