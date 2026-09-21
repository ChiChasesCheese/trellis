%% trellis:begin %%
# 上下文变量（contextvars）：为什么线程局部存储在 `await` 之间会失效
*asyncio 异步编程*

理解 `ContextVar` 按任务隔离而不是按线程隔离、每个 Task 在创建时复制当前 Context、`decimal` 上下文与追踪 ID 如何借此跨 await 传播，以及 `threading.local` 在 asyncio 里为何出错。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/asyncio.coroutines-tasks|协程、`await` 与 `Task`：调用协程函数只得到协程对象]]

## Readings
- [[peps-context-variables|PEP 567：上下文变量（contextvars）]]
- [[pydocs-contextvars|contextvars：按任务隔离的上下文变量]]

## Cards (6)
1. [[context-var-set-get-across-await-example]]
2. [[contextvar-isolated-by-task-not-thread]]
3. [[contextvar-must-be-module-level-not-closure]]
4. [[contextvar-set-returns-token-for-reset]]
5. [[task-copies-context-at-creation]]
6. [[threading-local-bleeds-across-tasks-same-thread]]
%% trellis:end %%

## Notes
