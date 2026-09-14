---
id: analytics-derived-data-framing
node: analytics.derived
type: qa
---
## Q
What distinguishes a "system of record" from "derived data", and why does the distinction change how you operate each?

## A
- **System of record**: the authoritative first write; if it's lost, the data is gone. Must be durable, transactional, carefully protected.
- **Derived data**: any transformation of it — caches, search indexes, materialized views, warehouse tables, ML features. Lost or corrupted? **Recompute it from the source.**

Operational consequences: derived stores can be rebuilt at will (so schema/mapping changes are cheap — build new, swap), can be eventually consistent, and there can be many of them, each shaped for one read pattern. Trouble starts when a store's role is ambiguous — nobody knows if it can be safely dropped and rebuilt. Related: [[storage-search-not-sot]].

## Q zh
什么区别"记录系统"和"派生数据"，为什么区别改变你如何操作每个？

## A zh
- **记录系统**：权威的第一次写；如果丢失，数据就消失。必须持久、事务性、仔细保护。
- **派生数据**：它的任何转换 — 缓存、搜索索引、物化视图、warehouse 表、ML 特征。丢失或损坏？**从源重新计算。**

操作后果：派生 store 随时可以重建（所以 schema/mapping 变化便宜 — 构建新、交换），可能最终一致，可能有很多，每个为一个读模式成形。麻烦开始当 store 角色模糊 — 没人知道它是否能被安全地丢弃和重建。
