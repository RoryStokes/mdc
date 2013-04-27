import entity

class Building(entity.Entity):
  def __init__(self, x, y):
    super(Building, self).__init__(x, y, 1000)