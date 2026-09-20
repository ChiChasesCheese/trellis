---
nodes: [concurrency.asyncio]
url: https://docs.python.org/3/library/asyncio-sync.html
---
# Synchronization Primitives

值得读：asyncio 版 `Lock`/`Event`/`Condition`/`Semaphore` 的官方文档，对应
`concurrency-asyncio-lock`、`concurrency-asyncio-never-block-loop` 两张卡——这些原语协调的是协程而不是操作系统线程，
文档特意强调"不是线程安全的、不能跨线程用"，读它能补上为什么线程版的锁不能直接搬进协程代码里。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/asyncio-sync.html)

## Archived copy
![[pydocs-asyncio-sync-clip]]
%% trellis:end %%
