---
nodes: [asyncio.streams-protocols]
url: https://www.manning.com/books/python-concurrency-with-asyncio
tags: [book, no-archive]
title: Python Concurrency with asyncio · 第 8 章 流（Streams）
---
# Python Concurrency with asyncio · 第 8 章 流（Streams）

这一章深入 `StreamReader`/`StreamWriter` 这套高层网络 API：如何按行或按固定长度读取数据、背压（backpressure）是怎么通过 `drain()` 体现的，以及协议解析中常见的『粘包/半包』问题。

**读时提取：**
- `StreamReader.readline`/`readexactly` 分别适合什么协议格式
- `writer.drain()` 如何体现背压，防止写入速度超过对端处理速度
- 为什么基于流的协议解析要自己处理消息边界（长度前缀或分隔符）

%% trellis:begin %%
## Source
[Open the original ↗](https://www.manning.com/books/python-concurrency-with-asyncio)
%% trellis:end %%
