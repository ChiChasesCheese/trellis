---
id: craft-lock-hierarchy-and-reentrancy-3-intentional-rlock
node: craft.architecture.lock-hierarchy-and-reentrancy
type: qa
step: 3
---
## Q
**调用方向与可重入 · 双式记账为什么有理由用 RLock**｜架构

账本的 `reverse`（冲正）要「检查原分录存在，再写一条取反的新分录」，这两步必须在同一个临界区里；写新分录要调用 `post`，而 `post` 自己也拿同一把锁。这时 `Lock` 和 `RLock` 各会怎样？这个 `RLock` 和上一张里掩盖问题的 `RLock` 有什么区别？

## A
**要点。** 这是有意识的重入：`reverse` 持锁调用的是自己这个类的方法 `post`，控制权没有离开本类，不变量由同一段代码维护，不会暴露半状态。普通锁下这会直接自锁。判据：重入发生在同一个类内部的自调用，并且调用链上没有外部代码，才是合理的 `RLock`；一旦调用链上有回调、订阅者、用户传入的函数，就不要靠重入过关。

```python
class Ledger:
    def __init__(self, lock) -> None:
        self._lock = lock
        self.journal: list[str] = []

    def post(self, entry_id: str) -> None:
        with self._lock:
            if entry_id not in self.journal:
                self.journal.append(entry_id)

    def reverse(self, entry_id: str, new_id: str) -> None:
        with self._lock:                                # 检查原分录存在 + 写入冲正，必须在同一个临界区
            assert entry_id in self.journal
            self.post(new_id)             # 自调用：同一线程重入

for name, lock in (("Lock ", threading.Lock()), ("RLock", threading.RLock())):
    led = Ledger(lock)
    led.post("e1")
    t = threading.Thread(target=led.reverse, args=("e1", "r1"), daemon=True)
    t.start(); t.join(0.3)
    print(name, "reverse 调 post:", "卡死" if t.is_alive() else f"完成 {led.journal}")
```

先 `post("e1")` 再 `reverse("e1", "r1")`，`Lock` 与 `RLock` 各跑一次（0.3 秒内没结束判定卡死），实际输出：

```
Lock  reverse 调 post: 卡死
RLock reverse 调 post: 完成 ['e1', 'r1']
```

**为什么。** 另一种写法是拆出一个不拿锁的内部方法 `_post_locked`，由 `post` 和 `reverse` 各自在锁内调用，不需要重入。这样的好处是读代码就知道哪些方法持锁；代价是要多写一个方法，并约定「_locked 后缀表示调用方须已持有锁」。

**易错。** 重入加条件等待要格外小心：`Condition.wait()` 会把 `RLock` 的所有层级一次释放，外层方法醒来后以为自己一直持有锁，其实等待期间别的线程已经改过数据。遇到「重入 + 条件等待」，先拆成不拿锁的内部方法。
