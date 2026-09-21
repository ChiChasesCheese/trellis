---
nodes: [concurrency.gil, concurrency.threads, concurrency.multiprocessing, concurrency.choosing]
url: https://www.fluentpython.com/
tags: [book, no-archive]
title: Fluent Python 2e · 第 19 章 Python 的并发模型
---
# Fluent Python 2e · 第 19 章 Python 的并发模型

这一章综述 GIL 存在时线程、进程、协程三种并发方式各自适合什么场景：GIL 让同一时刻只有一个线程执行 Python 字节码，所以线程适合 I/O 密集型、进程适合 CPU 密集型、协程适合大量并发 I/O 且切换成本要低。

**读时提取：**
- GIL 为什么让多线程对 CPU 密集型任务没有加速效果
- I/O 密集型选线程/协程、CPU 密集型选多进程，这个经验法则背后的原因
- 线程切换、进程切换、协程切换在开销上的量级差异（不编数字，只记住相对关系）

%% trellis:begin %%
## Source
[Open the original ↗](https://www.fluentpython.com/)
%% trellis:end %%
