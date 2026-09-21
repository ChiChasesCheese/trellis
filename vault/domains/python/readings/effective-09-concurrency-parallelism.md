---
nodes: [concurrency.threads, concurrency.locks-races, concurrency.queues, concurrency.executors, asyncio.blocking-and-threads]
url: https://effectivepython.com/
tags: [book, no-archive]
title: Effective Python 3e · 第 9 章 并发与并行
---
# Effective Python 3e · 第 9 章 并发与并行

这一章区分『并发』（交替处理多个任务）和『并行』（同时执行），讲 GIL 下线程为什么只适合 I/O 密集型、用 `Lock` 防止数据竞争、用 `Queue` 在线程间安全传递工作项，以及 `ThreadPoolExecutor` 如何把这套模式打包成一个简单接口。

**读时提取：**
- 并发与并行的区别：交替执行 vs 真正同时执行
- `threading.Lock` 保护的是共享可变状态，不加锁的数据竞争长什么样
- `queue.Queue` 作为线程安全的生产者-消费者通道
- 把阻塞 I/O 扔进线程池、用 `asyncio` 统一调度的模式

%% trellis:begin %%
## Source
[Open the original ↗](https://effectivepython.com/)
%% trellis:end %%
