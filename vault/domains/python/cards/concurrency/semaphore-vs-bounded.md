---
id: semaphore-vs-bounded
node: concurrency.locks-races
type: qa
source: python-docs
---
## Q
`Semaphore` 和 `BoundedSemaphore` 有什么区别？分别用在什么场景？

## A
两者都维护一个内部计数器，`acquire()` 减一（计数器为 0 时阻塞），`release()` 加一，典型用途是限制同时访问某个有限资源（如数据库连接池）的线程数。区别在于 `BoundedSemaphore` 会检查计数器是否超过了初始值，一旦某处代码多调用了一次 `release()`（编程错误）就立刻抛出 `ValueError`；普通 `Semaphore` 不做这个检查，多余的 `release()` 会被悄悄接受，掩盖了 bug。因此用信号量限制固定容量资源时应优先用 `BoundedSemaphore`。
