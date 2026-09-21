---
id: lock-vs-rlock
node: concurrency.locks-races
type: qa
source: python-docs
---
## Q
`threading.Lock` 和 `threading.RLock`（可重入锁，reentrant lock）的核心区别是什么？为什么需要 RLock？

## A
`Lock` 不记录“谁持有”，同一个线程再次 `acquire()` 一把自己已持有的 `Lock` 会自己把自己阻塞死。`RLock` 内部记录“持有线程”和“递归层数”，同一线程可以多次 `acquire()` 而不阻塞，只有调用与 `acquire()` 次数相同的 `release()` 后锁才真正释放。当一个函数会递归调用自己、或调用另一个也需要同一把锁的函数时，必须用 `RLock`，否则会立即死锁。
