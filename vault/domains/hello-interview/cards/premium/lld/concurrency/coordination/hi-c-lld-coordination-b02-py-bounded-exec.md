---
id: hi-c-lld-coordination-b02-py-bounded-exec
node: lld.concurrency.coordination.beyond
type: qa
step: 2
---
## Q
**并发协调 · Python：线程池的内部队列是无界的**｜拓展 · 加分

`ThreadPoolExecutor` 看起来已经是"线程池加队列"了，直接用有什么隐患？怎么加背压？

## A
**模式。** 有界执行器（bounded executor）：用信号量限制在途任务数。

```python
import threading
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Callable


class BoundedExecutor:
    def __init__(self, workers: int, max_pending: int) -> None:
        self._ex = ThreadPoolExecutor(workers)
        self._slots = threading.BoundedSemaphore(max_pending)

    def submit(self, fn: Callable, *a, timeout: float | None = None) -> Future:
        if not self._slots.acquire(timeout=timeout):    # 满了：阻塞，或超时后拒绝
            raise TimeoutError("queue full")
        try:
            fut = self._ex.submit(fn, *a)
        except BaseException:
            self._slots.release()
            raise
        fut.add_done_callback(lambda _: self._slots.release())   # 成功或异常都归还名额
        return fut

    def shutdown(self) -> None:
        self._ex.shutdown(wait=True)


gate = threading.Event()
ex = BoundedExecutor(workers=1, max_pending=2)
ex.submit(gate.wait)
ex.submit(gate.wait)
try:
    ex.submit(gate.wait, timeout=0.1)       # 第三个被拒绝，而不是无限排队
    raise SystemExit("should reject")
except TimeoutError:
    pass
gate.set()
ex.shutdown()
```
- **隐患：** 它的工作队列是不限大小的简单队列，生产快于消费时内存无限增长，和无界队列同一个问题
- **做法：** 信号量计数"已提交未完成"，满了就让提交方阻塞或拒绝
- **完成回调里归还：** 即使任务抛异常也能释放，否则名额会泄漏
- **何时不用：** 任务数天然有限的批处理
