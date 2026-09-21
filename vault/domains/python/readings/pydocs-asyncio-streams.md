---
nodes:
- asyncio.streams-protocols
title: asyncio Streams：高层网络 I/O
corpus: python-docs
section: 36-asyncio-stream
url: https://docs.python.org/3/library/asyncio-stream.html
tags:
- canonical
---

# asyncio Streams：高层网络 I/O

StreamReader/StreamWriter 是 asyncio 里做网络编程最省心的高层 API，open_connection() 一步建立 TCP 连接并返回这一对读写对象，比直接用底层 Protocol 回调简单得多。文档给出了完整的 TCP 回显客户端/服务端示例，以及一个抓取 HTTP 响应头的实用例子。特别要注意背压（backpressure）机制：writer.write() 只是把数据放进内部缓冲区，真正等待数据发送完毕、避免无限堆积内存要调用 await writer.drain()，很多人写爬虫或代理时忘记 drain 导致内存暴涨就是这个原因。这篇文档配合分页拉取 API 时如何做并发限流的模式（Semaphore 限并发加失败重试）是写异步网络客户端最常用的组合，比自己手搓 socket 处理省心得多。
