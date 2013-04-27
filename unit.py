import node

class Unit(object):
    def __init__(self, x, y):
        super(Node, self).__init__()

        self.x, self.y = float(x), float(y)
        self.dir = 0

    def pathTo(self, board, node):
        currentNode = Node(self.x, self.y)

        path = board.get_shortest_path(currentNode, node)

        #Now do something with the path... perhaps move somewhere?

    def draw(self):
        #Draw the unit...
        pass

    def visibleNodes(self, board):
        currentNode = Node(self.x, self.y)
        
        return board.get_visible_set(currentNode)

    def canSee(self, board, node):
        nodeList = visibleNodes(board)

        return node in nodeList