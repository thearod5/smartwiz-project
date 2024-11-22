import queue
import time
from typing import Generic, TypeVar

import threading

ItemType = TypeVar("ItemType")


class RateLimitedQueue(Generic[ItemType]):
    def __init__(self, items_per_minute: int):
        """
        Synchronized queue with limited rate per limit.
        :param items_per_minute: How many items per minute are allowed.
        """
        self.queue = queue.Queue()
        self.items_per_minute = items_per_minute
        self.lock = threading.Lock()
        self.last_access_time = None
        self.interval = 60.0 / items_per_minute if items_per_minute else None

    def __len__(self) -> int:
        """
        :return: Returns the length of the queue.
        """
        return self.queue.unfinished_tasks

    def put(self, item: ItemType) -> None:
        """
        Adds item to queue.
        :param item: The item to add.
        :return: None
        """
        self.queue.put(item)

    def get(self) -> ItemType:
        """
        Gets the next item in the queue.
        :return: Returns next item in the queue.
        """
        if self.interval is None:
            return None if self.queue.qsize() == 0 else self.queue.get()
        with self.lock:
            if self.queue.qsize() == 0:
                return None
            elapsed_time = time.time() - self.last_access_time if self.last_access_time else self.interval
            if elapsed_time < self.interval:
                sleep_time = self.interval - elapsed_time
                time.sleep(sleep_time)
            if self.queue.qsize() == 0:
                return None
            self.last_access_time = time.time()
            item = self.queue.get()
            return item

    def increment_interval(self, delta: float) -> None:
        """
        Increments the expected seconds per request.
        :param delta: The delta to increase interval by.
        :return: None
        """
        self.interval += delta
