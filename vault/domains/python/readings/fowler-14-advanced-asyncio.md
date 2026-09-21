---
nodes: [asyncio.futures, asyncio.event-loop]
url: https://www.manning.com/books/python-concurrency-with-asyncio
tags: [book, no-archive]
title: Python Concurrency with asyncio · 第 14 章 进阶 asyncio：自定义可等待对象与事件循环内部
---
# Python Concurrency with asyncio · 第 14 章 进阶 asyncio：自定义可等待对象与事件循环内部

这一章讲实现 `__await__` 自己写一个可等待对象需要满足什么协议，以及事件循环内部是怎么把『就绪的回调』排进队列逐个执行的，帮助理解 `await` 语法糖底下真正发生了什么。

**读时提取：**
- 自定义可等待对象需要实现的 `__await__` 协议是什么样的生成器协议
- 事件循环内部如何维护一个就绪回调队列，逐个执行直到队列暂时清空再去轮询 I/O
- `Future` 和协程的关系：协程最终 resolve 成的其实是底层的 Future

%% trellis:begin %%
## Source
[Open the original ↗](https://www.manning.com/books/python-concurrency-with-asyncio)
%% trellis:end %%
