---
id: hi-c-lld-scarcity-b02-py-fifo-sem
node: lld.concurrency.scarcity.beyond
type: qa
step: 2
---
## Q
**并发稀缺资源 · Python：先进先出的加权信号量**｜拓展 · 加分

按资源单位计许可的信号量，怎样既不饿死大请求，又不让永远满足不了的请求卡死？

## A
**模式。** 加权信号量（weighted semaphore）加排队凭证。

```python
import threading
import time
from collections import deque


class WeightedSemaphore:
    def __init__(self, total: int) -> None:
        self._total, self._free = total, total
        self._cond = threading.Condition()
        self._line: deque[object] = deque()          # 排队的凭证，队首优先

    def acquire(self, n: int) -> None:
        if n > self._total:
            raise ValueError("request exceeds total budget")   # 永远满足不了：直接拒绝
        ticket = object()
        with self._cond:
            self._line.append(ticket)
            while self._line[0] is not ticket or self._free < n:
                self._cond.wait()
            self._line.popleft()
            self._free -= n
            self._cond.notify_all()                  # 让新的队首重新检查

    def release(self, n: int) -> None:
        with self._cond:
            self._free += n
            self._cond.notify_all()


ws = WeightedSemaphore(10)
order: list[str] = []
ws.acquire(8)


def big() -> None:
    ws.acquire(9)
    order.append("big")
    ws.release(9)


def small() -> None:
    ws.acquire(1)
    order.append("small")
    ws.release(1)


tb = threading.Thread(target=big)
tb.start()
time.sleep(0.1)                                      # 保证 big 先排队
ts = threading.Thread(target=small)
ts.start()
time.sleep(0.1)
assert order == []                                   # small 放得下（还剩 2），也要排在 big 后面
ws.release(8)
tb.join(5)
ts.join(5)
assert order == ["big", "small"]
```
- **为什么用凭证：** 只有队首可以检查是否满足，避免谁先醒来谁先抢造成的饥饿
- **代价：** 队首大请求等待时，剩余容量闲置，吞吐略降；严格公平和高吞吐不可兼得
- **`notify_all` 的原因：** 唤醒的线程必须是新队首，单个 `notify` 可能唤醒一个不是队首的线程而丢失唤醒
- **何时不用：** 许可都是 1 时用标准 `Semaphore` 就够
