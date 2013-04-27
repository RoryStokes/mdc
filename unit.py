from node import Node

class Unit(object):
    def __init__(self, x, y):
        super(Unit, self).__init__()

        self.x, self.y = float(x), float(y)
        self.target = Node(x, y)
        self.path = []
        self.speed = 2
        self.dir = 0

    def pathTo(self, board, node):
        currentNode = Node(self.x, self.y)

        self.path = board.get_shortest_path(currentNode, node)
        self.target = self.path.pop(0)

    def update(self):
        reached = True

        if self.x > self.target.x:
            self.x -= self.speed
            reached = False
        elif self.x < self.target.x:
            self.x += self.speed
            reached = False
        
        if self.y > self.target.y:
            self.y -= self.speed
            reached = False
        elif self.y < self.target.y:
            self.y += self.speed
            reached = False

        if reached:
            if len(self.path) > 0:
                self.target = self.path.pop(0)

    def visibleNodes(self, board):
        currentNode = Node(self.x, self.y)
        
        return board.get_visible_set(currentNode)

    def canSee(self, board, node):
        nodeList = visibleNodes(board)

        return node in nodeList

    def pos(self):
        return (int(self.x), int(self.y))