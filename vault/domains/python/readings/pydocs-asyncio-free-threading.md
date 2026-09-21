---
nodes:
- concurrency.free-threading
- asyncio.blocking-and-threads
title: asyncio 与自由线程 Python
corpus: python-docs
section: 38-asyncio-threading
url: https://docs.python.org/3/library/asyncio-threading.html
tags:
- canonical
---

# asyncio 与自由线程 Python

这篇文档讨论了 asyncio 在无 GIL（自由线程）构建下的行为变化：原本很多 asyncio 内部数据结构隐式依赖 GIL 提供的原子性保护，在自由线程构建下这层保护消失了，asyncio 库本身已经针对性加了必要的锁来保证线程安全，但使用者如果在多个真正并行的线程里各自跑事件循环、并试图跨线程直接操作 Task/Future 等对象，仍然需要格外小心。文档给出了一个跨线程生产者消费者的例子，展示正确的做法是用 asyncio.run_coroutine_threadsafe() 把跨线程调用安全地转交给事件循环所在的线程，而不是直接从别的线程操作事件循环内部对象。这是自由线程构建逐渐成熟后，asyncio 使用者需要更新的心智模型：单线程时代反正只有一个线程在跑的隐含假设不再绝对成立。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/asyncio-threading.html)

## Archived copy
![[pydocs-asyncio-free-threading-clip]]
%% trellis:end %%
