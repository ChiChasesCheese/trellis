---
nodes: [asyncio.event-loop, asyncio.coroutines-tasks, asyncio.gather-wait-timeout, asyncio.blocking-and-threads]
url: https://www.fluentpython.com/
tags: [book, no-archive]
title: Fluent Python 2e · 第 21 章 异步编程
---
# Fluent Python 2e · 第 21 章 异步编程

这一章是 asyncio 的整体入门：事件循环如何在单线程里通过协作式调度切换协程，`asyncio.create_task` 如何把协程包装成可并发调度的 `Task`，`gather` 如何收集多个任务的结果，以及阻塞调用为什么必须扔进线程池而不能直接 `await`。

**读时提取：**
- 事件循环是协作式调度：协程主动让出控制权（`await`），不是抢占式的
- `asyncio.create_task` 和直接 `await` 协程在『何时开始并发执行』上的区别
- `asyncio.gather` 如何并发运行多个协程并按顺序收集结果
- 阻塞式调用（如同步网络库）必须放进 `run_in_executor`，否则会卡住整个事件循环

%% trellis:begin %%
## Source
[Open the original ↗](https://www.fluentpython.com/)
%% trellis:end %%
