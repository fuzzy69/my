from queue import Queue
from typing import Any


class SetQueue(Queue):
    """Set collection that accepts only unique items
    https://stackoverflow.com/a/16506527"""

    def _init(self, maxsize: int):
        self.queue = set()

    def _put(self, item: Any):
        """Adds item to a queue"""
        self.queue.add(item)

    def _get(self) -> Any:
        """Removes and returns first item from queue"""
        return self.queue.pop()


if __name__ == "__main__":
    from collections import Counter
    from random import randrange

    c = Counter()
    sq = SetQueue()
    for i in range(100):
        sq.put(randrange(5))
    while not sq.empty():
        item = sq.get()
        c[item] += 1

    assert all(list(map(lambda x: x[1] == 1, c.most_common())))
