

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