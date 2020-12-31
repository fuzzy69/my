from queue import PriorityQueue
from threading import Lock


class UniquePriorityQueue:
    """Priority queue wrapper which accepts the same values only once"""

    def __init__(self, maxsize: int = 0):
        self._queue = PriorityQueue(maxsize)
        self._values = set()
        self._lock = Lock()

    def put(self, item: tuple):
        """Puts priority/value tuple pair to queue"""
        _, value = item
        with self._lock:
            if value not in self._values:
                self._queue.put(item)
                self._values.add(value)

    def multi_put(self, items: list):
        """Puts multiple priority/value tuple pairs to queue"""
        with self._lock:
            for item in items:
                _, value = item
                if value not in self._values:
                    self._queue.put(item)
                    self._values.add(value)

    def get(self) -> tuple:
        """Returns priority/value tuple pair to queue"""
        with self._lock:
            return self._queue.get()

    def task_done(self):
        """Notify queue that task is complete"""
        with self._lock:
            self._queue.task_done()

    def empty(self) -> bool:
        """Returns true is queue is empty otherwise False"""
        with self._lock:
            return self._queue.empty()


if __name__ == "__main__":
    from collections import Counter
    from random import randrange

    c = Counter()
    upq = UniquePriorityQueue()
    previous_items = set()
    # Fill the queue
    for i in range(10):
        upq.put((0, i))
        previous_items.add(i)
    # Empty the queue
    while not upq.empty():
        _, item = upq.get()
    # Fill the queue
    for i in range(20):
        upq.put((0, i))
    # Items in queue shouldn't be in a previously added items collection
    while not upq.empty():
        _, item = upq.get()
        assert item not in previous_items
