---
nodes: [concurrency.gil, concurrency.threads, concurrency.multiprocessing, asyncio.event-loop]
url: https://realpython.com/products/cpython-internals-book/
tags: [book, no-archive]
title: CPython Internals · 并行与并发
---
# CPython Internals · 并行与并发

这一部分从解释器实现角度讲 GIL 存在的原因（保护引用计数这类非原子操作不被多线程同时修改破坏），以及线程、进程、协程三条并发路径在 CPython 里分别对应什么底层机制。

**读时提取：**
- GIL 存在的根本原因：保护引用计数等解释器内部状态不被多线程同时修改破坏
- 多进程如何靠『每个进程一份解释器状态』完全绕开 GIL
- asyncio 的协作式调度为什么天然不需要 GIL 之外的额外同步

%% trellis:begin %%
## Source
[Open the original ↗](https://realpython.com/products/cpython-internals-book/)
%% trellis:end %%
