---
id: analytics-replica-analytics-limits
node: analytics.olap
type: qa
---
## Q
"Why buy a warehouse? Just point the analysts at a read replica of the production database." Give the reasons this stops working as analytics grows up.

## A
- **Wrong storage layout**: the replica is still a row-store with OLTP indexes — a scan-and-aggregate over 100M rows does orders of magnitude more I/O than a column store, and no amount of hardware changes the layout.
- **Workload interference by design**: analytical queries hold long snapshots, which on MVCC engines blocks cleanup (Postgres vacuum horizon), bloats storage, and inflates replication lag — analysts degrade the *production* system from the "read-only" side.
- **Wrong schema**: the schema is normalized for application writes and riddled with app-specific encodings; analysts want wide, denormalized, history-preserving tables (facts/dimensions, slowly changing history the OLTP schema overwrites in place).
- **One database is never enough**: real analysis joins orders with support tickets, ad spend, and clickstream — data from *many* systems. A replica of one OLTP database structurally can't hold that; the warehouse's job is integration under one query engine.

The replica trick is fine at small scale; the exit sign is analysts throttling production (lag/vacuum alarms) or asking cross-system questions.

## Q zh
"买什么数据仓库？让分析师直接查生产库的只读副本不就行了。"给出随着分析需求成熟，这个方案逐渐失效的原因。

## A zh
- **存储布局就是错的**：副本仍然是带着 OLTP 索引的行存——对 1 亿行做扫描聚合，比列存多出数量级的 I/O，堆硬件也改变不了布局。
- **负载干扰是结构性的**：分析查询持有长快照，在 MVCC 引擎上会卡住清理（Postgres 的 vacuum horizon）、膨胀存储、拉大复制滞后——分析师从"只读"一侧照样拖垮*生产*系统。
- **schema 就是错的**：schema 为应用写入而规范化，充满应用私有的编码；分析师要的是宽的、反规范化的、保留历史的表（事实/维度表、OLTP schema 会原地覆盖掉的缓变历史）。
- **一个库永远不够**：真正的分析要把订单和客服工单、广告投放、点击流连起来——数据来自*许多*系统。单个 OLTP 库的副本在结构上装不下这些；仓库的本职就是在一个查询引擎下完成整合。

小规模时副本方案没问题；退出信号是分析师开始拖累生产（lag/vacuum 告警），或开始问跨系统的问题。
