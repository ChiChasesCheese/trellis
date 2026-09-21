---
nodes:
- asyncio.streams-protocols
title: asyncio Transports 与 Protocols：底层网络 API
corpus: python-docs
section: 37-asyncio-protocol
url: https://docs.python.org/3/library/asyncio-protocol.html
tags:
- canonical
---

# asyncio Transports 与 Protocols：底层网络 API

这是比 Streams 更底层的网络 API，用回调风格（类似 Twisted）而不是协程风格处理 I/O：Transport 负责实际的字节读写，Protocol 定义收到数据、连接建立/断开时该做什么（connection_made、data_received、connection_lost 等回调方法）。文档区分了流式协议（基于字节流，如 TCP）和数据报协议（基于独立数据包，如 UDP），以及只读/只写/子进程等特化 Transport。这套 API 是 Streams 高层封装的实现基础，绝大多数业务代码不需要直接用它，但理解它能解释为什么 Streams 的读写是 await 风格而底层却是回调风格，是 asyncio 在高层 API 上做的语法糖包装。文末给出了 TCP/UDP 回显服务器和 loop.subprocess_exec() 结合 SubprocessProtocol 管理子进程的完整例子。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/asyncio-protocol.html)

## Archived copy
![[pydocs-asyncio-transports-protocols-clip]]
%% trellis:end %%
