---
id: craft-lock-hierarchy-and-reentrancy-1-callback-under-lock
node: craft.architecture.lock-hierarchy-and-reentrancy
type: qa
step: 1
---
## Q
**调用方向与可重入 · 持锁时通知订阅者，会出什么事**｜架构

记账服务新增一笔支出后要通知订阅者（比如刷新界面），订阅者拿到通知后习惯回头调用 `debts()` 读最新账本。通知如果写在持锁的临界区里，订阅者回头读账本时：用普通锁（`Lock`）会怎样？换成可重入锁（`RLock`）呢？

## A
**要点。** 持锁回调外部代码，等于把自己的临界区交给别人的代码决定长短，有两类风险。用 `Lock`：订阅者在同一线程里再拿同一把锁，永远等不到，死锁。用 `RLock`：同一线程可以重复进入，死锁没了，但订阅者读到的是改了一半的状态，不变量暴露了。可重入锁掩盖了设计问题。

```python
class Ledger:
    def __init__(self, lock) -> None:
        self._lock = lock
        self.debts_ab = 0
        self.expenses = 0
        self.subscribers = []

    def debts(self) -> tuple[int, int]:
        with self._lock:
            return self.debts_ab, self.expenses

    def add_expense(self, amount: int) -> None:
        with self._lock:
            self.debts_ab += amount                    # 1. 先改债务
            for s in self.subscribers:                 # 2. 持锁回调外部代码
                s(self)
            self.expenses += 1                         # 3. 再记笔数：半状态窗口就在 2 之前

def run(lock, name: str) -> None:
    led = Ledger(lock)
    seen: list = []
    led.subscribers.append(lambda l: seen.append(l.debts()))   # 订阅者回头读账本
    t = threading.Thread(target=led.add_expense, args=(30,), daemon=True)
    t.start(); t.join(0.3)
    if t.is_alive():
        print(f"{name}: 死锁，同一线程重复拿不可重入的锁")
    else:
        print(f"{name}: 订阅者读到 (债务, 笔数) =", seen[0], "-> 债务已加、笔数还没加")

run(threading.Lock(), "Lock ")
run(threading.RLock(), "RLock")
```

订阅者在回调里调用 `l.debts()`，`Lock` 和 `RLock` 各跑一次（0.3 秒内没结束就判定卡死），实际输出：

```
Lock : 死锁，同一线程重复拿不可重入的锁
RLock: 订阅者读到 (债务, 笔数) = (30, 0) -> 债务已加、笔数还没加
```

**为什么。** `RLock` 里的「重入」只在同一线程内部自调用时成立；一旦控制权交到不受控的外部代码，重入就不再是你想要的东西。

**易错。** 症状在 `RLock` 下比 `Lock` 更隐蔽：不会卡死，数据悄悄错。正确做法是把通知移到锁外，只在锁内构造事件。
