---
nodes: [asyncio.sync-primitives, concurrency.locks-races]
url: https://www.manning.com/books/python-concurrency-with-asyncio
tags: [book, no-archive]
title: Python Concurrency with asyncio · 第 11 章 同步原语
---
# Python Concurrency with asyncio · 第 11 章 同步原语

这一章讲 asyncio 里的 `Lock`/`Semaphore`/`Event`/`Condition` 和线程版本同名但语义略有差异：它们协调的是协程之间的执行顺序，不需要处理『抢占式中断』这种线程特有的问题，但共享可变状态时依然需要显式同步。

**读时提取：**
- asyncio 的 `Lock` 和 `threading.Lock` 在语义和使用场景上的差异
- `asyncio.Event` 如何让多个协程等待某个条件被设置后再继续
- 即使协作式调度『看起来安全』，跨 `await` 点的共享状态仍然可能出现竞态

%% trellis:begin %%
## Source
[Open the original ↗](https://www.manning.com/books/python-concurrency-with-asyncio)
%% trellis:end %%
