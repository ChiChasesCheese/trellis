---
id: hl-j16-reentrantlock-abilities
node: java21.j16-concurrency-primitives
type: qa
step: 26
---
## Q
`ReentrantLock` 比 `synchronized` 多出哪些能力？各对应什么 API？

## A
| 能力 | 代码 |
|---|---|
| 尝试获取，不阻塞 | `lock.tryLock()` |
| 带超时 | `lock.tryLock(100, TimeUnit.MILLISECONDS)` |
| 可被中断地等待 | `lock.lockInterruptibly()` |
| 公平锁（先来先得） | `new ReentrantLock(true)` |
| 多个条件队列 | `lock.newCondition()`（`synchronized` 只有一个 `wait/notify`） |
| 非块结构（不同方法里加/解锁） | `lock()` / `unlock()` 分开调用 |

`tryLock(超时)` 是避免死锁的常用办法：拿不到就退让。**可重入**（reentrant）：同一线程可重复获取，计数记录，`unlock` 同样次数才真正释放。
