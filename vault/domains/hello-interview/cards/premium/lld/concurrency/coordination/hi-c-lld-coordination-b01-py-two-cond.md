---
id: hi-c-lld-coordination-b01-py-two-cond
node: lld.concurrency.coordination.beyond
type: qa
step: 1
---
## Q
**并发协调 · Python：两个条件变量的有界缓冲**｜拓展 · 加分

`queue.Queue` 的底层是什么？自己写一个有界缓冲，用两个条件变量避免惊群，怎么写？

## A
**模式。** 有界缓冲（bounded buffer）：一把锁，两个条件。

```python
import threading
from collections import deque


class BoundedBuffer:
    def __init__(self, cap: int) -> None:
        self._q: deque = deque()
        self._cap = cap
        lock = threading.Lock()
        self._not_empty = threading.Condition(lock)   # 两个条件共用一把锁
        self._not_full = threading.Condition(lock)

    def put(self, item) -> None:
        with self._not_full:
            while len(self._q) >= self._cap:           # while：醒来要重查
                self._not_full.wait()
            self._q.append(item)
            self._not_empty.notify()                   # 只唤醒一个消费者

    def get(self):
        with self._not_empty:
            while not self._q:
                self._not_empty.wait()
            item = self._q.popleft()
            self._not_full.notify()                    # 只唤醒一个生产者
            return item


buf, out = BoundedBuffer(2), []
STOP = object()                                        # 毒丸


def consumer() -> None:
    while (x := buf.get()) is not STOP:
        out.append(x)


ts = [threading.Thread(target=consumer) for _ in range(3)]
for t in ts:
    t.start()
for i in range(100):
    buf.put(i)
for _ in ts:
    buf.put(STOP)                                      # 每个消费者一颗
for t in ts:
    t.join(timeout=5)
assert sorted(out) == list(range(100))
```
- **标准库：** `queue.Queue` 正是这个结构：一把互斥锁加 `not_empty`、`not_full`、`all_tasks_done` 三个条件
- **`Condition(lock)`：** 多个条件可以共用同一把锁，所以放入与取出互斥
- **配套：** `task_done()` 与 `join()` 用于等所有任务处理完；Python 3.13 起 `Queue.shutdown()` 提供内置的停机语义
- **何时不用：** 自己实现只在要自定义语义时；否则用标准库
