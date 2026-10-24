---
id: pl-conc-locks-pitfall-reentrancy
node: concurrency.locks-shared-memory
type: qa
step: 10
---
## Q
同一个线程对同一把锁连续加锁两次会怎样？Go、Python、Java、Rust 的表现各是什么？这个坑常出现在什么代码里？

## A
这取决于锁是否**可重入**：

Go（`sync.Mutex` 不可重入）：
```go
var mu sync.Mutex
mu.Lock()
mu.Lock() // not reentrant
```
输出：`fatal error: all goroutines are asleep - deadlock!`，`goroutine 1 [sync.Mutex.Lock]:`。

Python：
```python
l = threading.Lock(); l.acquire()
l.acquire(timeout=0.2)    # False: still held by ourselves
r = threading.RLock(); r.acquire()
r.acquire(timeout=0.2)    # True: same thread may re-enter
```
输出：`Lock second acquire: False`、`RLock second acquire: True`（没有 `timeout` 的 `Lock.acquire()` 会永远卡住）。

Java：`synchronized` 与 `ReentrantLock` 都可重入，嵌套加锁成功，`ReentrantLock` 记录持有次数（`getHoldCount()` 为 2），要解锁同样的次数；其他线程 `tryLock()` 则得到 `false`。

Rust：`Mutex` 不可重入，同一线程再次 `lock()` 的结果标准库不作保证（可能死锁，也可能 panic）；想探测可以用 `try_lock()`，它会返回 `Err`。

典型出现场景：一个加锁的公开方法 `a()` 调用了另一个同样加锁的公开方法 `b()`。可重入锁让这样的代码「恰好能跑」，不可重入锁则当场暴露设计问题。常见的修法是拆成「加锁的外部方法」和「假设已持锁的内部方法」（如 Go 里的 `xxxLocked`）。

另一个更经典的死锁：线程 1 先锁 A 再锁 B，线程 2 先锁 B 再锁 A。对策是所有线程按固定的全局顺序加锁。
