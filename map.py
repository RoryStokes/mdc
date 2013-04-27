import geometry
import mapping
from node import Node

print "start"
top_left_inner = geometry.Polygon((4, 10), (10, 4), (10, 10),
                               ccw=False)
print "1"
top_right_inner = geometry.Polygon((22,4), (28,10), (22,10),
								ccw=False)
bot_left_inner = geometry.Polygon((4,22), (10,28), (4,28),
								ccw=False)
bot_right_inner = geometry.Polygon((22,22), (28,22), (22,28),
								ccw=False)

bot_left_outer = geometry.Polygon((0,25),(0,32),(32,32),
								ccw=False)
bot_right_outer = geometry.Polygon((32,25),(32,32),(25,32),
								ccw=False)

river_top = geometry.Polygon((0,13),(32,13),(32,14),(0,14),
								ccw=False)
river_bot = geometry.Polygon((0,18),(32,18),(32,19),(0,19),
								ccw=False)


print "polys made"
terrain_map = mapping.Board()

terrain_map.add(top_left_inner)
terrain_map.add(top_right_inner)
terrain_map.add(bot_left_inner)
terrain_map.add(bot_right_inner)
terrain_map.add(bot_left_outer)
terrain_map.add(bot_right_outer)
print "map done"