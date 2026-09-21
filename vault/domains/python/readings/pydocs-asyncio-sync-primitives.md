---
nodes:
- asyncio.sync-primitives
title: asyncio 同步原语：Lock / Semaphore / Event / Barrier
corpus: python-docs
section: 31-asyncio-sync
url: https://docs.python.org/3/library/asyncio-sync.html
tags:
- canonical
---

# asyncio 同步原语：Lock / Semaphore / Event / Barrier

asyncio 提供了和 threading 同名但语义不同的同步原语家族：asyncio.Lock、Event、Condition、Semaphore、BoundedSemaphore、Barrier。关键点是，即使 asyncio 程序通常运行在单线程里，跨 await 点的临界区依然可能被其他协程插入执行，所以单线程就不需要加锁的直觉在异步代码里是错的：两个协程可能交替执行同一段逻辑，中间的 await 就是切换点。Semaphore 最常见的用法是限制同时在途的并发请求数（比如最多 10 个并发 HTTP 请求），避免打爆下游服务。这些同步原语专为事件循环设计，不能跨线程使用，如果需要协调线程和协程，要用线程安全的 asyncio.run_coroutine_threadsafe() 而不是直接共享这些对象。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/asyncio-sync.html)

## Archived copy
![[pydocs-asyncio-sync-primitives-clip]]
%% trellis:end %%
