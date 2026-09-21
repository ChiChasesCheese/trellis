---
id: task-copies-context-at-creation
node: asyncio.contextvars
type: qa
source: python-docs
---
## Q
一个 `asyncio.Task` 内部对 `ContextVar` 的修改，会不会影响到创建它之后才启动的其它并发任务？

## A
不会。每个 `Task` 在被创建的那一刻，会拿当前上下文（context）做一份快照（`contextvars.copy_context()`）保存成自己的 `_context`，之后这个 Task 的协程体始终跑在这份属于自己的上下文副本里；Task 内部对 `ContextVar.set()` 的修改只体现在这份副本中，不会传播到其它任务或者外层代码。
