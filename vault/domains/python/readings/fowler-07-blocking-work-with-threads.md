---
nodes: [asyncio.blocking-and-threads, concurrency.threads]
url: https://www.manning.com/books/python-concurrency-with-asyncio
tags: [book, no-archive]
title: Python Concurrency with asyncio · 第 7 章 用线程处理阻塞任务
---
# Python Concurrency with asyncio · 第 7 章 用线程处理阻塞任务

这一章讲对于阻塞式但不是 CPU 密集型的调用（如某些同步 I/O 库），正确做法是扔进线程池而不是进程池：线程间共享内存，不需要序列化结果，开销比进程小得多。

**读时提取：**
- 阻塞 I/O 调用为什么优先选线程池而不是进程池（共享内存、无需序列化）
- `run_in_executor` 默认使用的线程池和显式传入自定义 `ThreadPoolExecutor` 的区别
- 线程池大小该如何根据阻塞调用的并发量来设置

%% trellis:begin %%
## Source
[Open the original ↗](https://www.manning.com/books/python-concurrency-with-asyncio)
%% trellis:end %%
