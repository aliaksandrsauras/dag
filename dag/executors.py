import logging
import multiprocessing
import threading

logger = logging.getLogger(__name__)

NOT_AVAILABLE = "N/A"


class ThreadedExecutor:
    def __init__(self, max_workers=None):
        self.max_workers = max_workers
        self.lock = threading.Lock()
        self.threads = []

    def execute(self, queue):
        if self.max_workers is None:
            self.max_workers = self.calc_max_workers(queue)

        self.threads = []
        for _ in range(self.max_workers):
            th = threading.Thread(target=self._task, args=(queue,), daemon=True)
            th.start()
            self.threads.append(th)

        queue.join()  # should be encapsulated and made non-blocking if included into a web app

    def _task(self, queue):
        while True:
            node = queue.get()

            if node.value is None:
                params = [n.value for n in node.ins]
                if NOT_AVAILABLE in params:
                    node.value = NOT_AVAILABLE
                else:
                    try:
                        node.value = node.operator(params)
                    except Exception:
                        node.value = NOT_AVAILABLE
                        logger.exception(
                            "Error occurred while performing node %s evaluation",
                            node.node_id,
                        )

            with self.lock:
                for out_node in node.outs:
                    out_node.evaluated_ins += 1
                    if out_node.evaluated_ins == len(out_node.ins):
                        queue.put(out_node)

            queue.task_done()

    @staticmethod
    def calc_max_workers(queue):
        result = queue.qsize()
        cpu_count = multiprocessing.cpu_count()
        if result > cpu_count:
            result = cpu_count

        return result
