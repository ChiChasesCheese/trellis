---
id: uth-compose-connection-pool-3-invariants-code
node: compose.connection-pool
type: qa
step: 3
---
## Q
**不变量与最小实现**｜HikariCP · 7.0.2

三个结构要保持一致。写一个最小的 `ConcurrentBag`，说清借还的顺序。

## A
**不变量。**

- 同一个连接任何时刻只有一个线程能把它从「空闲」抢成「在用」，所以不会借给两个人。
- `sharedList` 含有全部连接；本地列表和交接队列里的只是「提示」，可能已经过期，所以借出前必须再抢一次状态。

**顺序。** 借：本地 → 共享 → 在交接队列上等。还：先把状态改回空闲，再看有没有人在等，有就交给他。

```python
import queue
import threading
import time


class Conn:
    def __init__(self) -> None:
        self.busy = threading.Lock()                         # 锁着 = 在用；acquire(False) 相当于 CAS(空闲 -> 在用)


class Bag:
    def __init__(self) -> None:
        self.shared: list[Conn] = []                         # 全部连接，不管空闲还是在用
        self.mine = threading.local()                        # 线程本地：本线程上次用过的连接
        self.handoff: queue.Queue[Conn] = queue.Queue()      # 交接队列：借不到的线程在这里等
        self.waiting: list[None] = []                        # 在等的线程；append / pop 在 CPython 里是原子的

    def borrow(self, timeout: float) -> Conn:
        last: Conn | None = getattr(self.mine, "last", None)
        for c in ([last] if last else []) + self.shared:     # 1 先试本线程上次用的，2 再扫全部连接
            if c.busy.acquire(False):
                return c
        self.waiting.append(None)                            # 3 都被借走：登记后在交接队列上等
        end = time.monotonic() + timeout
        try:
            while True:                                      # 超时由 get 抛出 queue.Empty
                c = self.handoff.get(timeout=max(0.0, end - time.monotonic()))
                if c.busy.acquire(False):                    # 交来的连接可能已被别人抢走，抢不到就接着等
                    return c
        finally:
            self.waiting.pop()

    def requite(self, c: Conn) -> None:
        self.mine.last = c                                   # 记住：下次这个线程先找它
        c.busy.release()                                     # 在用 -> 空闲
        if self.waiting:                                     # 有人在等：交给他
            self.handoff.put(c)
```

**坑。** 先交接、后改状态，对方会拿到一个还显示「在用」的连接。示例用锁模拟 CAS：`acquire(False)` 抢到就相当于 CAS 成功。

**对应 LeetCode：** 无直接对应的题
