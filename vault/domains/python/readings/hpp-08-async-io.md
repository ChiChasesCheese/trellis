---
nodes: [asyncio.event-loop, concurrency.choosing]
url: https://www.oreilly.com/library/view/high-performance-python/9781492055013/
tags: [book, no-archive]
title: High Performance Python 2e · 第 8 章 异步 I/O
---
# High Performance Python 2e · 第 8 章 异步 I/O

这一章讲异步 I/O 用单线程 + 事件循环处理大量并发连接，靠的是操作系统的多路复用（如 epoll）而不是每个连接一个线程，讨论了它相对多线程在高并发 I/O 场景下的优势和边界。

**读时提取：**
- 事件循环靠操作系统多路复用（epoll 之类）同时监控大量连接
- 异步 I/O 相比每连接一线程节省了什么开销（线程栈、上下文切换）
- 异步 I/O 的短板：一旦某个协程做了阻塞调用会拖慢整个事件循环

%% trellis:begin %%
## Source
[Open the original ↗](https://www.oreilly.com/library/view/high-performance-python/9781492055013/)
%% trellis:end %%
