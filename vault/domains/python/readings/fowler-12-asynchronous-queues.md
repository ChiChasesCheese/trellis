---
nodes: [asyncio.sync-primitives, concurrency.queues]
url: https://www.manning.com/books/python-concurrency-with-asyncio
tags: [book, no-archive]
title: Python Concurrency with asyncio · 第 12 章 异步队列
---
# Python Concurrency with asyncio · 第 12 章 异步队列

这一章讲 `asyncio.Queue` 如何实现协程版的生产者-消费者模式：`put`/`get` 在队列满/空时会挂起而不是阻塞线程，`task_done`/`join` 则用来等待队列里的工作全部处理完。

**读时提取：**
- `asyncio.Queue` 的 `put`/`get` 在队列满/空时如何挂起当前协程而不阻塞事件循环
- `task_done()` 和 `queue.join()` 配合，如何等待所有已入队任务被消费完
- 多个消费者协程从同一个队列取任务，如何做到负载自动均衡

%% trellis:begin %%
## Source
[Open the original ↗](https://www.manning.com/books/python-concurrency-with-asyncio)
%% trellis:end %%
