from node import Node
import math, entity

class Unit(entity.Entity):
    def __init__(self, x, y, board):
        super(Unit, self).__init__(x, y, 100)

        self.target = Node(x, y)
        self.path = []
        self.speed = 0.05
        self.dir = 0
        self.radius = 0.5
        self.board = board.get_expanded(-0.5)

    def pathTo(self, moveToPos):
        currentNode = Node(self.x, self.y)
        targetNode = Node(moveToPos[0], moveToPos[1])

        testPath = self.board.get_shortest_path(currentNode, targetNode)
        if testPath != None:
            self.path = testPath
            self.target = self.path.pop(0)

        print(str(currentNode))
        print(str(targetNode))

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
                self.target = self.path.pop(0)
