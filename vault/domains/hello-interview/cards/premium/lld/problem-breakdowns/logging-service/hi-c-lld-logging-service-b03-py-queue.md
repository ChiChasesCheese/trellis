---
id: hi-c-lld-logging-service-b03-py-queue
node: lld.problem-breakdowns.logging-service.beyond
type: qa
step: 4
---
## Q
**日志库 · Python：有界队列加哨兵的异步目的地**｜拓展 · 加分

异步写在 Python 里怎么最小地实现？溢出和关闭各自怎么落到代码上？

## A
**模式。** 生产者-消费者加哨兵关闭（poison pill）。

```python
import queue
import threading
from typing import Callable

_STOP = object()                              # 哨兵：放进队列表示"没有更多了"


class AsyncDestination:
    def __init__(self, write: Callable[[str], None], capacity: int = 1000) -> None:
        self._q: queue.Queue = queue.Queue(maxsize=capacity)   # 有界：背压点
        self.dropped = 0                       # 溢出计数，要暴露成指标
        self._write = write
        self._t = threading.Thread(target=self._drain, name="log-drain")
        self._t.start()

    def emit(self, line: str) -> None:
        try:
            self._q.put_nowait(line)           # 不阻塞调用方
        except queue.Full:
            self.dropped += 1                  # 丢新的：宁可丢日志，不能拖慢业务；多生产线程下 += 非原子，计数只是近似

    def _drain(self) -> None:
        while (item := self._q.get()) is not _STOP:
            try:
                self._write(item)              # 唯一消费者：不需要锁
            except Exception:
                pass

    def close(self) -> None:
        self._q.put(_STOP)                     # 哨兵排在已有记录之后，所以先排空再停
        self._t.join()


out: list[str] = []
a = AsyncDestination(out.append, capacity=5)
for i in range(3):
    a.emit(f"r{i}")
a.close()
assert out == ["r0", "r1", "r2"]               # 关闭前的记录都写出了，顺序不变

gate = threading.Event()
slow = AsyncDestination(lambda s: gate.wait(), capacity=2)   # 消费者卡住
for i in range(10):
    slow.emit(f"x{i}")
print("dropped", slow.dropped)                 # 队列满了之后的都被丢弃
gate.set(); slow.close()
```
- **`put_nowait` 加 `queue.Full`：** 实现"丢新记录"策略；换成 `put(timeout=…)` 就是"限时阻塞"，换成先 `get_nowait()` 再 `put` 则是"丢最旧"。
- **哨兵：** 用 `object()` 做唯一标记，放在已有记录之后，消费者读到才停，所以一定先排空；比"设置一个停止标志再等队列空"少一个竞态。
- **单消费者免锁：** 只有 `_drain` 线程碰 sink。`dropped += 1` 在多个生产线程下不是原子的，要精确计数就加锁。
- **标准库对应：** `logging.handlers.QueueHandler` 加 `QueueListener` 就是这个结构。
- **何时不用：** 日志量很低、延迟不敏感时，同步加每目的地一把锁更简单，也不会在崩溃时丢缓冲。
