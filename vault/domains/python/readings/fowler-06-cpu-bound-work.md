---
nodes: [asyncio.blocking-and-threads, concurrency.multiprocessing]
url: https://www.manning.com/books/python-concurrency-with-asyncio
tags: [book, no-archive]
title: Python Concurrency with asyncio · 第 6 章 处理 CPU 密集型任务：配合进程池
---
# Python Concurrency with asyncio · 第 6 章 处理 CPU 密集型任务：配合进程池

这一章讲 CPU 密集型代码放进协程会独占事件循环、饿死其他任务，正确做法是用`run_in_executor` 把它扔进 `ProcessPoolExecutor`，绕开 GIL 在另一个进程里真正并行计算，再把结果 `await` 回主协程。

**读时提取：**
- CPU 密集型代码直接写在协程里为什么会卡住整个事件循环，而不只是卡住自己
- `loop.run_in_executor` 如何把同步/CPU 密集型调用委托给线程池或进程池
- 为什么 CPU 密集型要选进程池而不是线程池（绕开 GIL）

%% trellis:begin %%
## Source
[Open the original ↗](https://www.manning.com/books/python-concurrency-with-asyncio)
%% trellis:end %%
