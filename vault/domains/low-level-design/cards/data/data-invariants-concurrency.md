---
id: data-invariants-concurrency
node: data.invariants
type: qa
step: 8
---
## Q
单线程下 `transfer` 的不变量没问题。多线程调用时，什么情况下别的线程会看到不变量被破坏？锁要包住什么？

## A
**不变量只在不持锁时成立，锁要包住整个检查加修改**

- **中间状态**：`src -= n` 之后、`dst += n` 之前，总和少了 `n`；别的线程此刻读 `total()` 就看到破的状态；
- **check-then-act**：检查完 `bal[src] >= n`，另一线程已扣走了钱，随后的扣款把余额扣成负数；
- **GIL 不够**：它只保证单条字节码原子，`x -= n` 不是一条；
- **做法**：检查与两次写放在同一个 `with self._lock`，读 `total()` 也拿同一把锁；
- **例外**：构造后不再改的不可变状态不需要锁。

```python
import threading

class Bank:
    def __init__(self, balances):
        self._bal, self._lock = dict(balances), threading.Lock()
    def transfer(self, src, dst, n):
        with self._lock:                      # 检查与两次写在同一个临界区
            if n <= 0 or self._bal[src] < n:
                raise ValueError("bad transfer")
            self._bal[src] -= n
            self._bal[dst] += n
    def total(self):
        with self._lock:                      # 读也拿锁，看不到中间状态
            return sum(self._bal.values())
```

**知识点：**不变量与封装（Invariants）
