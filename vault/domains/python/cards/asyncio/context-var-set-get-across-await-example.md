---
id: context-var-set-get-across-await-example
node: asyncio.contextvars
type: qa
source: python-docs
---
## Q
`decimal` 模块的精度上下文（context）、分布式追踪的 trace ID 这类「每个任务各自一份」的状态，是怎样借助 `ContextVar` 在跨越多个 `await` 的一整条协程调用链里保持一致的？

## A
这类模块在自己内部用一个模块级的 `ContextVar` 作为「键」，通过 `set()`/`get()` 读写当前值；因为同一个 Task 从创建到结束运行在同一份上下文快照里，即使中途多次 `await` 把控制权交还事件循环、又被恢复执行，`get()` 拿到的值也始终是本任务这条调用链自己设置的那份，不会被并发跑着的其它任务的设置覆盖。
