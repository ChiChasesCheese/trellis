%% trellis:begin %%
# 连接池：HikariCP 的 ConcurrentBag
*数据结构组合：开源框架里的类设计*

借还连接要快、线程之间少抢：每个线程先看自己用过的连接（线程本地列表），再看共享列表，都没有就在交接队列上等别人归还；连接的状态用 CAS 切换。

**Core** — part of the first pass through this subject.

## Cards (4)
1. [[uth-compose-connection-pool-1-needs]]
2. [[uth-compose-connection-pool-2-structures]]
3. [[uth-compose-connection-pool-3-invariants-code]]
4. [[uth-compose-connection-pool-4-real]]
%% trellis:end %%

## Notes
