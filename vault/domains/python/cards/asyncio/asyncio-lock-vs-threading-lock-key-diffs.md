---
id: asyncio-lock-vs-threading-lock-key-diffs
node: asyncio.sync-primitives
type: qa
source: python-docs
---
## Q
`asyncio.Lock`（以及 `Semaphore`、`Event`、`Condition` 等）和 `threading.Lock` 相比，官方文档特别强调的两条差异是什么？

## A
第一，asyncio 的这些同步原语（synchronization primitives）不是线程安全（thread-safe）的，不能用来在多个 OS 线程之间同步，只能在同一个事件循环内协调协程/任务；第二，它们的方法不接受 `timeout` 参数，想要带超时的等待，需要另外套一层 `asyncio.wait_for()`。
