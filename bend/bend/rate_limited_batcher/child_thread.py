import logging
import threading
import time
from typing import Any, Callable

from rate_limited_batcher.constants import OVERLOADED_ERROR
from rate_limited_batcher.multi_thread_state import MultiThreadState


class ChildThread(threading.Thread):
    def __init__(self, state: MultiThreadState, thread_work: Callable):
        """
        Constructs a child thread for the multi-thread state.
        :param state: State containing synchronization information for child threads.
        :param thread_work: The work to be performed by the child thread.
        """
        super().__init__()
        self.state = state
        self.thread_work = thread_work

    def run(self) -> None:
        """
        Performs work on the next available items until no more work is available.
        :return: None
        """
        work = self.state.get_work()
        while work is not None:
            index, item = work
            work_result = self._perform_work(item, index)
            self.state.on_item_finished(work_result, index)
            work = self.state.get_work()

    def _perform_work(self, item: Any, index: int) -> Any:
        """
        Performs work on item.
        :param item: The item to perform work on.
        :param index: The index of the item.
        :return: The result of the work.
        """
        attempts = 0
        has_performed_work = False
        while not has_performed_work and self.state.should_attempt_work(attempts):
            if self.state.pause_work:
                time.sleep(self.state.sleep_time_on_error)
            if attempts > 0:
                logging.info(f"Re-trying request...")
            try:
                attempts += 1
                thread_result = self.thread_work(item)
                self.state.pause_work = False
                return thread_result
            except Exception as e:
                self._handle_exception(attempts, e, index)

    def _handle_exception(self, attempts: int, e: Exception, index: int) -> None:
        """
        Handles exception caused while performing work.
        :param attempts: The number of attempts on this current work.
        :param e: The exception thrown.
        :param index: The item's index
        :return: None
        """
        if not self.state.below_attempt_threshold(attempts):
            self.state.on_item_fail(e, index=index)
        else:
            self.state.on_valid_exception(e)
        if OVERLOADED_ERROR in str(e).lower():
            self.state.increase_interval()
