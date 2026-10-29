---
id: uth-compose-thread-pool-3-invariants-code
node: compose.thread-pool
type: qa
step: 3
---
## Q
**不变量与最小实现**｜Java ThreadPoolExecutor · JDK 21

三个结构要保持一致。写一个最小的线程池，说清 `execute` 的判断顺序和每一步改谁。

## A
**不变量。**

- 线程数是「预订」出来的：真实实现先在 `ctl` 上用 CAS（比较并交换，原子地改数字）加一占名额，再创建线程、放进 `workers`，创建失败要把名额还回去。
- 线程数没到 core，新任务总是优先新建线程，不排队。
- 只有队列满了，线程数才会涨到 core 以上，最多到 max。

**顺序。** 固定为：core → 入队 → max → 拒绝。新建工人时，任务直接交给它当第一个任务，不经过队列。

```python
import queue
import threading
from collections.abc import Callable


class MiniPool:
    def __init__(self, core: int, maximum: int, queue_size: int) -> None:
        self.core, self.maximum = core, maximum
        self.tasks: queue.Queue[Callable[[], None]] = queue.Queue(queue_size)   # 有界任务队列
        self.workers: set[threading.Thread] = set()          # 工人集合
        self.lock = threading.Lock()                         # Java 里线程数用 ctl 上的 CAS，集合另用 mainLock

    def execute(self, task: Callable[[], None]) -> None:
        with self.lock:
            if len(self.workers) < self.core:                # 1 不足 core：新建线程，任务当它的第一个任务
                return self._add_worker(task)
        try:
            self.tasks.put_nowait(task)                      # 2 入队，等空闲工人来取
        except queue.Full:
            with self.lock:
                if len(self.workers) >= self.maximum:        # 4 线程已到 max：拒绝
                    raise RuntimeError("rejected")
                self._add_worker(task)                       # 3 队列满了、还没到 max：再新建一个

    def _add_worker(self, first: Callable[[], None]) -> None:
        t = threading.Thread(target=self._run, args=(first,), daemon=True)
        self.workers.add(t)                                  # 调用方已持锁
        t.start()

    def _run(self, task: Callable[[], None]) -> None:
        while True:
            task()                                           # 先跑手里的任务，之后不停从队列取
            task = self.tasks.get()
```

**坑。** 示例省掉了空闲回收、关闭，也没处理任务抛异常；真实实现里工人因异常退出时，会补一个新工人。

**对应 LeetCode：** 无直接对应的题
