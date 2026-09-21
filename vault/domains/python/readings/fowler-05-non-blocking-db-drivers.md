---
nodes: [asyncio.sync-primitives]
url: https://www.manning.com/books/python-concurrency-with-asyncio
tags: [book, no-archive]
title: Python Concurrency with asyncio · 第 5 章 非阻塞数据库驱动
---
# Python Concurrency with asyncio · 第 5 章 非阻塞数据库驱动

这一章讲普通数据库驱动大多是同步阻塞的，直接在协程里调用会卡住整个事件循环；要么换用原生异步驱动，要么用连接池限制并发连接数，并用信号量类同步原语控制对数据库的并发访问上限。

**读时提取：**
- 为什么同步数据库驱动不能直接在协程里调用，否则会阻塞整个事件循环
- 连接池如何限制同时打开的数据库连接数，避免打垮数据库
- `asyncio.Semaphore` 用来给一批并发任务设置『最多同时几个』的上限

%% trellis:begin %%
## Source
[Open the original ↗](https://www.manning.com/books/python-concurrency-with-asyncio)
%% trellis:end %%
