import logging
import multiprocessing
import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
from multiprocessing.queues import Queue as TypeQueue
from typing import override


class QueueAlreadyClosedError(Exception):

    def __init__(self):
        super().__init__("Queue is already closed")


# https://stackoverflow.com/a/34293098/14778387
class CloseableQueue(TypeQueue):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._closed = False

    @staticmethod
    def new_instance(maxsize=1024) -> 'CloseableQueue':
        return CloseableQueue(
            maxsize=maxsize,
            ctx=multiprocessing.get_context())

    @override
    def put(self, obj, block=True, timeout=None):
        if self._closed:
            raise QueueAlreadyClosedError()

        super().put(obj, block, timeout)

    @override
    def get(self, block=True, timeout=None):
        if self._closed:
            raise QueueAlreadyClosedError()

        return super().get(block, timeout)

    @override
    def close(self):
        self._closed = True

    @property
    def is_closed(self) -> bool:
        return self._closed


# https://docs.python.org/3/library/logging.html#logrecord-attributes
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s (%(thread)s) - %(levelname)s - %(message)s")
logger = logging.getLogger()

queue = CloseableQueue.new_instance()


def worker(worker_id: int) -> None:
    logger.info(f"Worker {worker_id} started")
    is_running = True

    while is_running:
        try:
            item = queue.get(timeout=1)
            logger.info(f"Worker {worker_id} got {item}")

        except QueueAlreadyClosedError:
            logger.info(f"Queue is closed. Worker {worker_id} finished")
            is_running = False

        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            is_running = False

    logger.info(f"Worker {worker_id} finished")


def supplier(input_queue: TypeQueue) -> None:
    for i in range(10000):
        input_queue.put(i)
        logger.info(f"Put {i} into the queue")

    input_queue.close()


def main() -> None:
    threading.Thread(target=supplier, args=(queue,)).start()

    with ThreadPoolExecutor() as executor:
        executor.map(worker, range(2))


if __name__ == '__main__':
    logger.info('Application was started')
    start_time = time.time()
    main()
    logger.info(f'Application finished in {time.time() - start_time:.2f} seconds')
    logger.info('Application finished')
