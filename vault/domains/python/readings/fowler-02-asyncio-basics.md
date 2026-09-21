---
nodes: [asyncio.coroutines-tasks, asyncio.futures, asyncio.cancellation, asyncio.debugging]
url: https://www.manning.com/books/python-concurrency-with-asyncio
tags: [book, no-archive]
title: Python Concurrency with asyncio · 第 2 章 asyncio 基础：协程、任务、future 与调试
---
# Python Concurrency with asyncio · 第 2 章 asyncio 基础：协程、任务、future 与调试

这一章讲协程函数（`async def`）本身只是创建了一个协程对象，必须被 `await` 或包进`Task` 才会真正运行；`Future` 是『未来会有结果的占位符』这一层更底层的抽象；也讲了取消一个任务实际上是往里面抛 `CancelledError`，代码必须能正确处理它。

**读时提取：**
- 定义一个协程函数和真正运行它（`await`/`create_task`）是两个独立的步骤
- `Task` 是对协程的包装，让它能被事件循环并发调度
- 取消任务的本质：在其挂起点抛出 `CancelledError`，必须被协程自己处理或传播
- asyncio 的调试模式如何暴露『协程从未被 await』一类的常见错误

%% trellis:begin %%
## Source
[Open the original ↗](https://www.manning.com/books/python-concurrency-with-asyncio)
%% trellis:end %%
