---
id: concurrency-depth-connection-pool
node: concurrency-depth.safe-structures
type: qa
step: 4
---
## Q
写一个固定大小的连接池：最多 N 个调用方同时拿到连接，拿不到就等，用完一定归还。为什么用 `queue.Queue` 装空闲连接比 `list` 加 `Lock` 加 `Condition` 更好？归还要注意什么？

## A
**空闲连接放进 `queue.Queue`，归还写进 `finally`**

- **`Queue` 已经包含不变量**：`get()` 在空时阻塞，`put()` 唤醒等待者，阻塞和唤醒的细节（循环里等待、通知谁）不用自己写对；
- **池大小就是上限**：队列里放 N 个连接，同时被借走的不会超过 N；`get(timeout=…)` 超时抛 `queue.Empty`，示例里转成 `TimeoutError`，不要无限等；
- **借用写成上下文管理器**：`finally` 里归还，调用方抛异常也不会漏还；漏还的池子慢慢耗尽，最后全员阻塞；
- **坏连接**：示例没有处理；用完发现已断开，就换一个新的放回去，池里的数量保持 N；
- **不要把同一个连接归还两次**：队列里出现两份，两个调用方会同时拿到同一个连接。示例没有防护，要防就记一个“借出中”的集合，归还时检查。

```python
import queue
from contextlib import contextmanager

class Pool:
    def __init__(self, make, size):
        self._idle = queue.Queue()
        for _ in range(size):
            self._idle.put(make())
    @contextmanager
    def connection(self, timeout=1.0):
        try: conn = self._idle.get(timeout=timeout)
        except queue.Empty: raise TimeoutError("pool exhausted") from None
        try: yield conn
        finally: self._idle.put(conn)          # 异常也归还
```

**知识点：**线程安全结构的写法（Thread-Safe Structures）
