---
id: testing-flaky-barrier-invariant
node: testing.flaky
type: qa
step: 1
---
## Q
测试「8 个线程同时申请 ID，ID 不重复」时，线程一个个启动、先启动的早就跑完了，根本没有竞争；断言写成「线程 3 拿到 4」又时对时错。并发测试该怎么写才既有竞争又稳定？

## A
**屏障同时起跑，断言不变量，不断言谁赢**

- **`threading.Barrier(n)`**：每个线程到了屏障就等，凑齐 n 个才一起放行，竞争的窗口才真正存在；
- **断言集合，不断言分配**：8 个 ID 排序后恰好是 1 到 8，没有重复、没有缺号；谁拿到几号由调度决定，不该写进断言；
- **等待要带超时**：`join(timeout)` 加线程是否还活着的检查，死锁变成一次失败，而不是整个测试套件挂住；
- **结果收集用线程安全的容器**：`list.append` 是单个字节码级别的原子操作，这里够用；复杂的结果放 `queue.Queue`；
- **一次通过不算证明**：竞争条件靠概率暴露，把线程数和循环次数调大，用重复运行压一压。

```python
import threading
from itertools import count

lock, ids, out = threading.Lock(), count(1), []
def work():
    bar.wait(timeout=5)                  # 同时起跑
    with lock: out.append(next(ids))

bar = threading.Barrier(8)
ts = [threading.Thread(target=work) for _ in range(8)]
for t in ts: t.start()
for t in ts: t.join(timeout=5)
print(sorted(out) == list(range(1, 9)))   # True：断言集合，不断言谁拿几号
```

**知识点：**不稳定测试（Flaky Tests）
