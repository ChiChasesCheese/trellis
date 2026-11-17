---
id: concurrency-depth-green-proves-nothing
node: concurrency-depth.testing
type: qa
step: 3
---
## Q
一个没加锁的计数器，多线程测试在你的机器上稳定通过，能说明代码线程安全吗？怎么检查这个测试本身有没有用？

## A
**测试通过只说明没碰到，用“删掉锁”检验测试**

- **实测（3.11，4 线程各调 10000 次 `c.inc()`，`inc` 里是 `self.n += 1`，没有锁，300 轮）**：默认间隔和 1e-6 都是 0/300 轮丢计数；同一段代码在 3.14t 上是 300/300 轮丢；
- **原因**：3.11 里切换主要发生在函数入口和循环回跳处，`+=` 这个读改写碰巧没有切换点。这是 CPython 实现细节，不是代码对；
- **变异检查（mutation check）**：把锁删掉，重跑测试；测试仍然绿，说明它根本没覆盖这把锁。要么加大线程数和操作数，要么在缺口里造一个确定性切换点（用 `Event` 把线程停在缺口里），要么换到 free-threaded 构建上跑；
- **测试只能证伪**：红了是真有问题，绿了只是这一次没出事；
- **补上别的手段**：代码评审时数一数每个共享变量被哪把锁保护；CI 里同时跑 GIL 和 free-threaded 两个构建。

```python
import sys, threading

class Counter:
    def __init__(self): self.n = 0
    def inc(self): self.n += 1                # 没有锁

sys.setswitchinterval(1e-6)
c, barrier = Counter(), threading.Barrier(4)
def work():
    barrier.wait()
    for _ in range(10_000): c.inc()
ts = [threading.Thread(target=work) for _ in range(4)]
[t.start() for t in ts]; [t.join() for t in ts]
print(c.n == 40_000)                          # 3.11：True；3.14t：几乎总是 False
```

**知识点：**测试并发代码（Testing Concurrency）
