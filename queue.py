import heapq
import itertools

REMOVED = '<removed-task>'

class PriorityQueue:
    def __init__(self):
        self.hq = []
        self.counter = itertools.count()
        self.finder = {}

    def __len__(self):
        return len(self.finder)

    def add(self, item, priority=0):
        if item in self.finder:
            self.remove(item)
        count = next(self.counter)
        entry = [priority, count, item]
        self.finder[item] = entry
        heapq.heappush(self.hq, entry)

    def remove(self, item):
        entry = self.finder.pop(item)
        entry[2] = REMOVED

    def pop(self):
        while self.hq:
            priority, count, item = heapq.heappop(self.hq)
            if item is not REMOVED:
                del self.finder[item]
                return item
        raise KeyError('pop from an empty priority queue')
