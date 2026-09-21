---
nodes: [concurrency.multiprocessing, concurrency.executors]
url: https://www.oreilly.com/library/view/high-performance-python/9781492055013/
tags: [book, no-archive]
title: High Performance Python 2e · 第 9 章 multiprocessing 模块
---
# High Performance Python 2e · 第 9 章 multiprocessing 模块

这一章讲多进程如何绕开 GIL 获得真正的并行，代价是进程间通信必须显式序列化（`Queue`/`Pipe`/共享内存），以及 `ProcessPoolExecutor` 如何把这套模式包装成和线程池一致的接口。

**读时提取：**
- 多进程绕开 GIL 的原理：每个进程有自己的解释器和内存空间
- 进程间传数据必须走序列化（pickle），这对传大对象是明显开销
- 共享内存（`multiprocessing.shared_memory`）如何避免大数组的重复拷贝

%% trellis:begin %%
## Source
[Open the original ↗](https://www.oreilly.com/library/view/high-performance-python/9781492055013/)
%% trellis:end %%
