---
id: hi-c-lld-intro-b02-py-rlock
node: lld.concurrency.intro.beyond
type: qa
step: 2
---
## Q
**并发入门 · Python：Lock 不可重入，RLock 可以**｜拓展 · 加分

同一个类里一个加锁方法调用另一个加锁方法，会发生什么？`Lock` 和 `RLock` 在底层怎么区别？

## A
**模式。** 可重入锁（reentrant lock）。

```python
import threading


class Account:
    def __init__(self, lock) -> None:
        self._lock, self.bal = lock, 0

    def deposit(self, x: int) -> None:
        with self._lock:
            self.bal += x

    def deposit_twice(self, x: int) -> None:
        with self._lock:              # 外层已持锁
            self.deposit(x)           # 内层再拿同一把锁
            self.deposit(x)


plain = threading.Lock()
plain.acquire()
assert plain.acquire(timeout=0.1) is False    # 同一线程再拿一次：永远等自己
plain.release()

b = Account(threading.RLock())                # 记录持有线程与重入次数
b.deposit_twice(5)
assert b.bal == 10
```
- **`Lock`：** 只有"锁着/没锁"，同一线程再次获取会死锁，且可以由别的线程释放
- **`RLock`：** 记录持有者和计数，同线程可重复获取，释放同样次数才真正放开
- **更好的结构：** 公开方法加锁，调用不加锁的私有方法 `_deposit`，不依赖可重入
- **何时不用 `RLock`：** 它会掩盖设计问题，也略慢
- **`with` 的作用：** 异常时也保证释放
