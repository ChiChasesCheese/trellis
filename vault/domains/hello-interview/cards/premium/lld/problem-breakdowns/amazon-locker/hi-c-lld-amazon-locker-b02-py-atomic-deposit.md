---
id: hi-c-lld-amazon-locker-b02-py-atomic-deposit
node: lld.problem-breakdowns.amazon-locker.beyond
type: qa
step: 3
---
## Q
**快递柜 · Python：把"查找加占用"做成原子操作**｜拓展 · 加分

怎样证明锁真的保证了"只剩一个格口时只有一个存件成功"？锁该包住哪些语句？

## A
```python
import threading


class Comp:
    def __init__(self) -> None:
        self.occupied = False


class Locker:
    def __init__(self, comps: list[Comp]) -> None:
        self._comps = comps
        self._lock = threading.Lock()   # 一个柜点一把锁：格口少，争用可以忽略

    def deposit(self) -> Comp | None:
        with self._lock:                # with 保证异常时也释放
            c = next((c for c in self._comps if not c.occupied), None)
            if c is None:
                return None
            c.occupied = True           # 查找与占用在同一把锁内：别的线程看不到中间状态
            return c


lk = Locker([Comp()])
got: list[Comp | None] = []
threads = [threading.Thread(target=lambda: got.append(lk.deposit())) for _ in range(20)]
for t in threads:
    t.start()
for t in threads:
    t.join()
assert sum(g is not None for g in got) == 1   # 20 个线程抢 1 个格口，恰有 1 个成功
```
- **锁保护的是：** 格口的占用标志（以及码表）；"查找"和"置位"之间不能有别的线程插入。
- **没有锁会怎样：** 不会每次出错，而是偶尔两个线程都看到空位；这类 bug 难复现，所以要靠推理而不是靠测试证明。
- **进一步：** 开门这类慢的硬件调用不要放在锁里，免得一次慢调用堵住所有存取。
- **何时不用：** 单线程或单进程事件循环里一次只处理一个请求，就不需要。
