---
nodes: [asyncio.event-loop, asyncio.streams-protocols]
url: https://www.manning.com/books/python-concurrency-with-asyncio
tags: [book, no-archive]
title: Python Concurrency with asyncio · 第 3 章 第一个 asyncio 应用：套接字与事件循环
---
# Python Concurrency with asyncio · 第 3 章 第一个 asyncio 应用：套接字与事件循环

这一章通过手写一个基于套接字的服务器，展示事件循环具体是怎么工作的：注册文件描述符的读写事件、在事件就绪时唤醒对应的协程，为后面直接使用高层 `asyncio.start_server`打下机制基础。

**读时提取：**
- 事件循环如何通过操作系统的 I/O 多路复用得知某个套接字可读/可写
- 从『手写回调』过渡到『用协程 + await』如何让异步代码读起来更像同步代码
- 高层 streams API（`start_server`）相比裸 socket 编程省下了哪些样板代码

%% trellis:begin %%
## Source
[Open the original ↗](https://www.manning.com/books/python-concurrency-with-asyncio)
%% trellis:end %%
