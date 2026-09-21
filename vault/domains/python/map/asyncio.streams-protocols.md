%% trellis:begin %%
# 网络层：Streams、Transports/Protocols 与 aiohttp 类客户端的用法
*asyncio 异步编程*

理解高层 `open_connection`/`StreamReader` 与低层 Protocol 回调的分工、背压与 `drain()`，以及分页拉取 API 时并发限流与重试的组合模式。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/asyncio.sync-primitives|异步同步原语与限流：`Semaphore`、`Lock`、`Queue`]]

## Readings
- [[fowler-03-first-asyncio-application|Python Concurrency with asyncio · 第 3 章 第一个 asyncio 应用：套接字与事件循环]]
- [[fowler-08-streams|Python Concurrency with asyncio · 第 8 章 流（Streams）]]
- [[pydocs-asyncio-streams|asyncio Streams：高层网络 I/O]]
- [[pydocs-asyncio-transports-protocols|asyncio Transports 与 Protocols：底层网络 API]]

## Cards (6)
1. [[drain-below-watermark-does-not-yield-loop]]
2. [[open-connection-returns-reader-writer-64kib-default]]
3. [[paginated-fetch-semaphore-plus-retry-pattern]]
4. [[stream-write-drain-backpressure]]
5. [[streams-high-level-vs-transport-protocol-low-level]]
6. [[transport-how-protocol-which-bytes]]
%% trellis:end %%

## Notes
