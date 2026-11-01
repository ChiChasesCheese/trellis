---
id: hi-pt-kv-store-eviction-1-decouple
node: qb.lld.kv-store-eviction.points
type: qa
step: 1
---
## Q
**可配置淘汰策略的内存键值存储 · 三部件解耦**｜出自：可配置淘汰策略的内存键值存储 › 整体设计

设计内存键值存储（Redis-lite），要支持多种数据结构、可切换的淘汰策略和 TTL。核心怎么拆分？

## A
**要点。** 拆成三个互不知道对方内部的部件：存储层（`KVStore`，持有字典、容量、锁、时钟）、数据结构层（字符串用 `str`、列表用 `deque`、有序集合自写 `SortedSet`，各守自己的不变量）、淘汰策略（`EvictionPolicy`）。
**策略接口。** `on_insert`、`on_access`、`on_remove`、`victim`；策略只回答「谁是下一个受害者」，不碰数据。新增结构或策略都不改已有代码。
