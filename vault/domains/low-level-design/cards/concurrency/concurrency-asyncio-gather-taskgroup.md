---
id: concurrency-asyncio-gather-taskgroup
node: concurrency.asyncio
type: qa
step: 5
---
## Q
`asyncio.gather()` 和 `asyncio.TaskGroup`（3.11+）都能并发跑多个协程，其中一个失败时，两者对其余任务的处理有什么不同？

## A
`asyncio.gather(*coros)` 默认在第一个协程抛出异常时，把这个异常原样向上抛出，但**不会**取消其余还在运行的协程——它们会继续跑完，除非调用方自己额外处理；只有 `gather()` 这次调用本身被取消时，才会级联取消所有子任务。

`TaskGroup` 是更结构化的写法（结构化并发，structured concurrency）：`async with asyncio.TaskGroup() as tg: tg.create_task(...)`，一旦任意一个子任务抛出非 `CancelledError` 的异常，组里其余任务会被立刻取消，所有异常最后汇总成一个 `ExceptionGroup` 抛出。当几个任务逻辑上是"要么一起成功、要么一起放弃"时，`TaskGroup` 更安全；只有在明确希望"一个失败不影响其他任务继续跑完"时才用 `gather`。
