---
id: suppress-cancelled-error-requires-uncancel
node: asyncio.cancellation
type: qa
source: python-docs
---
## Q
如果协程确实想吞掉（不重新抛出）收到的 `CancelledError`，只用 `except CancelledError: pass` 够吗？

## A
不够，还必须额外调用 `task.uncancel()` 才能把取消状态彻底清除。因为 `TaskGroup`、`asyncio.timeout()` 这些结构化并发（structured concurrency）组件内部也是用取消机制实现的，如果只吞异常不调用 `uncancel()`，会让它们对这个任务的取消计数产生误判，导致行为异常。
