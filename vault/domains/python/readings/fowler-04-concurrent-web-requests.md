---
nodes: [asyncio.gather-wait-timeout]
url: https://www.manning.com/books/python-concurrency-with-asyncio
tags: [book, no-archive]
title: Python Concurrency with asyncio · 第 4 章 并发网络请求：gather、as_completed、超时
---
# Python Concurrency with asyncio · 第 4 章 并发网络请求：gather、as_completed、超时

这一章讲并发发起多个网络请求的几种收集方式：`gather` 等所有任务完成再统一返回结果，`as_completed` 按完成顺序逐个拿到结果，以及如何用 `asyncio.wait_for` 给单个任务加超时而不拖累整批请求。

**读时提取：**
- `asyncio.gather` 一次性等待多个协程，某一个失败时默认行为是什么
- `as_completed` 如何让你在结果一个个就绪时立刻处理，而不必等最慢的那个
- `wait_for` 超时后任务处于什么状态，需要显式处理 `TimeoutError`

%% trellis:begin %%
## Source
[Open the original ↗](https://www.manning.com/books/python-concurrency-with-asyncio)
%% trellis:end %%
