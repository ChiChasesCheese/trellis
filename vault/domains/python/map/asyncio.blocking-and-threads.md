%% trellis:begin %%
# 阻塞调用与线程的交界：`to_thread`、`run_in_executor`、`run_coroutine_threadsafe`
*asyncio 异步编程*

理解同步阻塞库会冻结事件循环、把它丢到线程池的两种 API、从线程回到事件循环的线程安全方式，以及 CPU 密集任务应交给进程池。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/asyncio.coroutines-tasks|协程、`await` 与 `Task`：调用协程函数只得到协程对象]], [[domains/python/map/concurrency.executors|`concurrent.futures`：`ThreadPoolExecutor` vs `ProcessPoolExecutor`、`map` 与 `as_completed`]]

## Readings
- [[effective-09-concurrency-parallelism|Effective Python 3e · 第 9 章 并发与并行]]
- [[fluent-21-async-programming|Fluent Python 2e · 第 21 章 异步编程]]
- [[fowler-06-cpu-bound-work|Python Concurrency with asyncio · 第 6 章 处理 CPU 密集型任务：配合进程池]]
- [[fowler-07-blocking-work-with-threads|Python Concurrency with asyncio · 第 7 章 用线程处理阻塞任务]]
- [[pydocs-asyncio-coroutines-tasks|asyncio：协程与任务完整参考]]
- [[pydocs-asyncio-dev-practices|asyncio 开发实践与调试]]
- [[pydocs-asyncio-eventloop-ref|asyncio 事件循环底层 API 参考]]
- [[pydocs-asyncio-free-threading|asyncio 与自由线程 Python]]

## Cards (6)
1. [[call-soon-threadsafe-for-touching-asyncio-from-other-thread]]
2. [[event-loop-single-thread-one-task-at-a-time]]
3. [[run-coroutine-threadsafe-returns-concurrent-future]]
4. [[to-thread-gil-limits-to-io-bound]]
5. [[to-thread-runs-blocking-call-off-loop]]
6. [[to-thread-vs-run-in-executor-choice]]
%% trellis:end %%

## Notes
