from threading import Lock
from typing import Any

try:
    from libs.my.core.collection.set_queue import SetQueue
except ModuleNotFoundError:
    from core.collection.set_queue import SetQueue


class UniqueQueue:
    """Set queue wrapper which accepts the same values only once"""

    def __init__(self, maxsize: int = 0):
        self._queue = SetQueue(maxsize)
        self._items = set()
        self._lock = Lock()

    def put(self, item: Any):
        """Puts priority/value tuple pair to queue"""
        has_item = True
        with self._lock:
            if item not in self._items:
                self._items.add(item)
                has_item = False
        if not has_item:
            self._queue.put(item)

    def get(self) -> Any:
        """Returns priority/value tuple pair to queue"""
        return self._queue.get()

    def task_done(self):
        """Notify queue that task is complete"""
        self._queue.task_done()

    def empty(self) -> bool:
        """Returns true is queue is empty otherwise False"""
        return self._queue.empty()

    def qsize(self) -> int:
        """Returns number of items in queue"""
        return self._queue.qsize()
