---
id: hi-c-lld-inventory-management-b01-callback-pending
node: lld.problem-breakdowns.inventory-management.beyond
type: qa
step: 2
---
## Q
**库存管理 · Python：锁内登记，锁外派发**｜拓展 · 加分

告警回调为什么不能在锁里执行？用 Python 怎么写出"锁内只登记通知，锁外才调用"？

## A
**模式。** 收集后派发（collect-then-dispatch）：持锁时只改内存状态并把要做的事打包成可调用对象，释放锁之后再执行。

```python
import threading
from functools import partial


class Naive:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.qty = 10
        self.listener = lambda: None

    def remove(self) -> None:
        with self.lock:
            self.qty -= 1
            self.listener()                      # 回调在锁内：监听器回头读库存就会等自己


class Pending:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.qty = 10
        self.listener = lambda q: None

    def remove_locked(self) -> list:
        self.qty -= 1
        return [partial(self.listener, self.qty)]   # 锁内只"登记"，把现成的调用打包返回

    def remove(self) -> None:
        with self.lock:
            fires = self.remove_locked()
        for fire in fires:                       # 锁外执行：监听器慢、抛异常、回头调仓库都不影响别人
            fire()

    def stock(self) -> int:
        with self.lock:
            return self.qty


n = Naive()
n.listener = lambda: n.lock.acquire(timeout=0.2) or print("naive: 回调想拿同一把锁，等不到（真实代码里这里就是死锁）")
n.remove()

p = Pending()
p.listener = lambda q: print("pending: 回调里读库存 =", p.stock())
p.remove()
```
- **`functools.partial`：** 把函数和当时的参数（此刻的库存值）绑成一个无参可调用对象。锁内绑定，锁外执行，所以回调拿到的是决定告警那一刻的数量，而不是执行时可能已变化的值。
- **为什么返回 `list` 而不是直接调用：** 这样外层（如持有两把锁的调拨）可以收集多个仓库的通知，在释放所有锁之后统一执行。
- **异常隔离：** 派发循环里每个回调最好单独 `try/except` 并记录，一个监听器的错误不应影响其他监听器，也不应让已完成的库存变更看起来像失败。
- **何时不用：** 回调极快、无 I/O、也不会回调进同一个对象时，锁内直接调用更简单；但很难保证未来的监听器满足这些条件。
