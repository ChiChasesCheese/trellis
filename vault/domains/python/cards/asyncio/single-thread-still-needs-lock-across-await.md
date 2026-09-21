---
id: single-thread-still-needs-lock-across-await
node: asyncio.sync-primitives
type: qa
source: python-docs
---
## Q
asyncio 程序始终只有一个线程在跑协程，为什么修改共享状态时还需要 `asyncio.Lock`？

## A
单线程不代表没有竞态：协作式调度下，一段代码只要在临界区内部执行了 `await`，就会把控制权交还给事件循环，事件循环完全可能趁这个空档去运行另一个也要修改同一份共享状态的协程；等第一个协程恢复时，它以为独占的状态其实已经被改过了。因此只要临界区跨越了至少一个 `await` 点，就需要用 `asyncio.Lock` 显式保护。
