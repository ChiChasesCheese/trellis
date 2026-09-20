---
nodes: [problems.components.lru-cache]
url: https://github.com/abhaypaswan/lld-python/tree/main/problems/lru-cache
---
# lld-python — lru-cache

值得读：三个自由来源里唯一原生 Python、带 pytest 套件的实现，用哈希表加手写双向链表做到
O(1)，`EvictionPolicy` 抽象出 LRU/LFU/FIFO 三种可插拔策略，时钟通过依赖注入传入（测试用
`FakeClock` 推进时间）；和本文的方向一致，是本文淘汰策略接口与线程安全讨论的主要参照。
它用 `abc.ABC` 定义策略基类、把统计（命中/未命中/淘汰）内建进 `Cache`，本文改用
`typing.Protocol`、把统计留给读者作为"扩展与追问"的练习——这两处不同都在"关键设计决策"里说明理由。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/abhaypaswan/lld-python/tree/main/problems/lru-cache)

## Archived copy
![[src-abhaypaswan-lru-cache-clip]]
%% trellis:end %%
