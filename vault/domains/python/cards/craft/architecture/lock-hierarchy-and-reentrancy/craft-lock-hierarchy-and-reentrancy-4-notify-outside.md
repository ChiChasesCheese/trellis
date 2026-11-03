---
id: craft-lock-hierarchy-and-reentrancy-4-notify-outside
node: craft.architecture.lock-hierarchy-and-reentrancy
type: qa
step: 4
---
## Q
**调用方向与可重入 · 通知怎样挪到锁外，订阅者又不会读到半成品**｜架构

记账服务在锁内改账本，再通知订阅者。要把通知挪到锁外，但订阅者可能很慢，也可能回头读账本。怎样让锁外通知既不卡住账本，又不让订阅者拿到改了一半的状态？

## A
**要点。** 锁内只做两件事：改状态、构造事件；通知在锁外发。事件自带订阅者需要的全部信息，订阅者不需要回头访问账本，所以即便读到的比事件新，也不会读到半成品。锁也不用可重入了，普通锁足够，订阅者回头读账本时拿一次锁、放一次锁。

```python
@dataclass(frozen=True)
class Event:
    summary: str
    amount: int                                   # 事件自带全部信息：订阅者不必回头读账本

class Ledger:
    def __init__(self) -> None:
        self._lock = threading.Lock()             # 不可重入，也不需要
        self.debt = 0
        self.expenses = 0
        self._subs = []

    def debts(self) -> tuple[int, int]:
        with self._lock:
            return self.debt, self.expenses

    def add_expense(self, amount: int) -> None:
        with self._lock:
            self.debt += amount
            self.expenses += 1
            event = Event(f"新增支出 {amount}", amount)   # 在锁内只构造事件
        for sub in list(self._subs):                      # 锁外通知
            sub(event)

led = Ledger()
log: list = []
led.subscribe = led._subs.append
led.subscribe(lambda e: log.append((e.summary, led.debts())))   # 订阅者回头读账本也不会死锁
t = threading.Thread(target=led.add_expense, args=(30,), daemon=True)
t.start(); t.join(1)
print("卡死" if t.is_alive() else "完成", log)
```

订阅者在回调里读 `led.debts()`，实际输出：

```
完成 [('新增支出 30', (30, 1))]
```

**为什么。** 债务和笔数在同一个临界区里一起改，回调时两个值已经一致：（30, 1）。通知用 `list(self._subs)` 拷贝订阅者列表，订阅者在回调里取消订阅也不会弄坏遍历。

**代价。** 锁外通知意味着通知与状态变更不是原子的：订阅者收到事件时，账本可能又变了；订阅者之间的接收顺序也不保证与变更顺序严格一致。对于需要严格顺序的场景，要给事件带序号，或者放进队列由单独线程发出。
