---
nodes: [amazon.amz-emergency-pubsub]
url: https://docs.python.org/3/library/heapq.html
---
# heapq — Heap queue algorithm（Python 标准库文档）

值得读：官方文档，讲小根堆的 `heappush` / `heappop` 都是 O(log n)，并专门有一节「优先队列实现说明」：用 `(优先级, 序号, 任务)` 三元组，序号保证同优先级先进先出，也避免两个任务比较大小时抛 `TypeError`。本题解异步信箱里的 `(-severity, seq, event)` 就是这个写法；文档没讲的是「队列有界、满了挤掉最不重要的那条」，那一步本题解用一次线性扫描加 `heapify` 实现，并在文中说明了代价。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/heapq.html)

## Archived copy
![[src-pythondocs-ttl-cache-clip]]
%% trellis:end %%
