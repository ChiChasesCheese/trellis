---
nodes: [concurrency.gil, concurrency.choosing, asyncio.event-loop]
url: https://www.manning.com/books/python-concurrency-with-asyncio
tags: [book, no-archive]
title: Python Concurrency with asyncio · 第 1 章 认识 asyncio
---
# Python Concurrency with asyncio · 第 1 章 认识 asyncio

这一章从 GIL 讲起，解释为什么 Python 的并发选择要分三条路（多线程、多进程、asyncio），以及 asyncio 的单线程协作式事件循环相比多线程在『大量 I/O 等待』场景下的优势：没有线程切换开销，也不需要为共享状态加锁。

**读时提取：**
- GIL 如何决定了多线程对 CPU 密集型任务没有加速效果
- 协作式调度（coroutine 主动让出）与抢占式线程调度的本质区别
- 什么信号说明一个问题适合 asyncio：大量并发、以等待 I/O 为主、单个任务计算量小

%% trellis:begin %%
## Source
[Open the original ↗](https://www.manning.com/books/python-concurrency-with-asyncio)
%% trellis:end %%
