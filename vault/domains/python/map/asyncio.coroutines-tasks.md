%% trellis:begin %%
# 协程、`await` 与 `Task`：调用协程函数只得到协程对象
*asyncio 异步编程*

掌握 `async def` 返回的协程必须被 await 或包成 Task 才会执行、`create_task` 立即调度、忘记 await 的"从未被等待"警告，以及 Task 是 Future 的子类。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/asyncio.event-loop|事件循环：单线程协作式多任务如何工作]]

**Unlocks:** [[domains/python/map/asyncio.futures|Future：可等待的占位符与回调]], [[domains/python/map/asyncio.gather-wait-timeout|并发组合：`gather`、`wait`、`wait_for`、`timeout` 与 `TaskGroup`]], [[domains/python/map/asyncio.sync-primitives|异步同步原语与限流：`Semaphore`、`Lock`、`Queue`]], [[domains/python/map/asyncio.blocking-and-threads|阻塞调用与线程的交界：`to_thread`、`run_in_executor`、`run_coroutine_threadsafe`]], [[domains/python/map/asyncio.contextvars|上下文变量（contextvars）：为什么线程局部存储在 `await` 之间会失效]]

## Readings
- [[cpy-asyncio-internals|异步生成器为什么会漏跑 finally，以及 Task 是怎么被追踪的]]
- [[fluent-21-async-programming|Fluent Python 2e · 第 21 章 异步编程]]
- [[fowler-02-asyncio-basics|Python Concurrency with asyncio · 第 2 章 asyncio 基础：协程、任务、future 与调试]]
- [[peps-pep492-async-await|PEP 492：async/await 语法与原生协程]]
- [[pydocs-asyncio-coroutines-tasks|asyncio：协程与任务完整参考]]
- [[pydocs-asyncio-overview|asyncio 概念全景：事件循环、协程与 Future]]

## Drills
- [[asyncio-fix-the-silent-async-script|Drill：一段拉分页 API 的 asyncio 脚本没有任何输出，找出三个 bug]]

## Cards (6)
1. [[calling-coroutine-function-only-builds-object]]
2. [[create-task-schedules-not-runs-synchronously]]
3. [[create-task-weak-reference-gc-risk]]
4. [[never-awaited-runtimewarning]]
5. [[task-inherits-future-except-set-result-exception]]
6. [[task-tracking-per-thread-linked-list-3-14]]
%% trellis:end %%

## Notes
