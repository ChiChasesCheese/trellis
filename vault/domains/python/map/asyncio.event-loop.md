%% trellis:begin %%
# 事件循环：单线程协作式多任务如何工作
*asyncio 异步编程*

理解事件循环维护就绪队列与 I/O 选择器（selectors）、协程在 `await` 处让出、CPU 密集代码会卡住整个循环，以及 `asyncio.run()` 创建并关闭循环。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/iteration.yield-from|`yield from` 与生成器的 `send`/`throw`/`close`]]

**Unlocks:** [[domains/python/map/asyncio.coroutines-tasks|协程、`await` 与 `Task`：调用协程函数只得到协程对象]]

## Readings
- [[cpyint-04-parallelism-concurrency|CPython Internals · 并行与并发]]
- [[fluent-21-async-programming|Fluent Python 2e · 第 21 章 异步编程]]
- [[fowler-01-getting-to-know-asyncio|Python Concurrency with asyncio · 第 1 章 认识 asyncio]]
- [[fowler-03-first-asyncio-application|Python Concurrency with asyncio · 第 3 章 第一个 asyncio 应用：套接字与事件循环]]
- [[fowler-14-advanced-asyncio|Python Concurrency with asyncio · 第 14 章 进阶 asyncio：自定义可等待对象与事件循环内部]]
- [[hpp-08-async-io|High Performance Python 2e · 第 8 章 异步 I/O]]
- [[pydocs-asyncio-eventloop-ref|asyncio 事件循环底层 API 参考]]
- [[pydocs-asyncio-overview|asyncio 概念全景：事件循环、协程与 Future]]
- [[pydocs-asyncio-runners|asyncio.run() 与 Runner]]

## Cards (5)
1. [[asyncio-run-lifecycle-soundbite]]
2. [[await-task-vs-await-coroutine-cede-control]]
3. [[cpu-bound-code-blocks-whole-loop]]
4. [[event-loop-debug-mode-100ms-threshold]]
5. [[event-loop-job-queue-model]]
%% trellis:end %%

## Notes
