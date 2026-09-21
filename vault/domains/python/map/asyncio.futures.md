%% trellis:begin %%
# Future：可等待的占位符与回调
*asyncio 异步编程*

理解 Future 表示尚未完成的结果、`set_result`/`set_exception` 唤醒等待者、`add_done_callback`，以及 `run_in_executor` 如何把线程结果桥接成 Future。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/asyncio.coroutines-tasks|协程、`await` 与 `Task`：调用协程函数只得到协程对象]]

## Readings
- [[fowler-02-asyncio-basics|Python Concurrency with asyncio · 第 2 章 asyncio 基础：协程、任务、future 与调试]]
- [[fowler-14-advanced-asyncio|Python Concurrency with asyncio · 第 14 章 进阶 asyncio：自定义可等待对象与事件循环内部]]
- [[pydocs-asyncio-futures|asyncio Future 对象参考]]
- [[pydocs-asyncio-overview|asyncio 概念全景：事件循环、协程与 Future]]

## Cards (6)
1. [[asyncio-future-vs-concurrent-futures-future]]
2. [[future-create-via-loop-not-direct-construct]]
3. [[future-done-callback-scheduled-not-sync]]
4. [[future-represents-status-not-computation]]
5. [[future-set-result-twice-raises]]
6. [[run-in-executor-bridges-thread-result-to-future]]
%% trellis:end %%

## Notes
