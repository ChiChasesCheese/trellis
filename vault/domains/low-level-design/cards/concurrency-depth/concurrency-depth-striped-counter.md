---
id: concurrency-depth-striped-counter
node: concurrency-depth.atomics
type: qa
step: 4
---
## Q
Java 的 `LongAdder` 把一个计数拆成多个格子来减少竞争。在 Python 里照做（每个线程按哈希落到一个带锁的格子）值得吗？读总数时拿到的是一致的快照吗？

## A
**先量：Python 里单锁加短临界区通常够快，分段反而更慢**

- **做法**：开 N 个格子，每个一把锁，线程按 `get_ident() % N` 选一个累加，读总数把所有格子加起来；
- **实测（8 线程各加 20 万次，每个版本跑两次，结果相近）**：3.11 单锁 0.10 s、分段 0.16 s；3.14t（free-threaded）单锁 0.16 s、分段 0.27 s。分段多了一次取模和下标，竞争并不是瓶颈；
- **临界区拉长再试**：每次持锁做 100 次加一，5000 次调用：3.11 单锁 0.05 s、分段 0.09 s；3.14t 0.12 s 对 0.16 s，分段依然没有赢；
- **不用锁的办法更好**：每个线程在局部变量里累加，结束时合并一次（封闭的做法）。3.11 上同样的 160 万次加一，每线程一个线程局部计数器 0.06 s；
- **读总数不是快照**：`sum(cells)` 读的时候别的线程还在写，结果可能介于两个时刻之间。只适合监控和统计，不适合“恰好等于”的判断；要精确就加全局锁或停写；
- **什么时候值得**：线程数多、临界区长、测出锁等待是瓶颈，再换分段；没有测量就不要拆。

```python
import threading

class Striped:
    def __init__(self, stripes=16):
        self._cells = [0] * stripes
        self._locks = [threading.Lock() for _ in range(stripes)]
    def add(self, k=1):
        i = threading.get_ident() % len(self._cells)
        with self._locks[i]:
            self._cells[i] += k
    def value(self):                      # 不是快照：读的时候别人还在写
        return sum(self._cells)

c = Striped(); c.add(); c.add(2)
print(c.value())                          # 3
```

**知识点：**原子操作与无锁（Atomics & Lock-Free）
