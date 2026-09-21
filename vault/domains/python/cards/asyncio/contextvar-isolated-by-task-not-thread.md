---
id: contextvar-isolated-by-task-not-thread
node: asyncio.contextvars
type: qa
source: python-docs
---
## Q
`contextvars.ContextVar` 和 `threading.local()` 隔离状态的「粒度」分别是什么？

## A
`threading.local()` 是按 OS 线程隔离的：同一线程里所有代码共享同一份值。`ContextVar` 是按上下文（本质上是按 `asyncio.Task`）隔离的：在同一个线程内并发跑着的多个 Task，各自拿到的是自己那份上下文快照里的值，即使它们同属一个线程也互不干扰。
