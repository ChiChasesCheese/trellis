---
id: analytics-backfill-cdc
node: analytics.derived
type: qa
---
## Q
You're standing up a new derived view (search index, feature store) from a database that already holds years of data. Why do you need two pipelines, and how do you stitch them without gaps or double-processing?

## A
CDC alone can't help: the log doesn't retain history back to the beginning, so you need a **backfill** (bulk load from a snapshot) *plus* the **CDC tail** for ongoing changes.

Stitching: take a consistent snapshot whose **log position is known** (e.g. Debezium's initial snapshot records the binlog offset; or a backup annotated with its LSN), bulk-load it, then start CDC **exactly at that offset**. Overlap is tolerated by making applies idempotent/upserts — replaying a change you already have converges to the same state.

Gap = missed updates forever; that's why "snapshot with known offset" is the load-bearing detail.

## Q zh
你从已有多年数据的数据库建立新的派生视图（搜索索引、feature store）。为什么需要两个管道，如何不带间隙或重复处理地拼接它们？

## A zh
CDC 单独无法帮助：日志不保留回到开始的历史，所以需要**回填**（从快照批量加载）*加*上**CDC 追尾**用于持续变化。

拼接：获取其**日志位置已知**的一致性快照（例如 Debezium 的初始快照记录 binlog offset；或用其 LSN 注释的备份），批量加载它，然后**恰好在那个 offset** 启动 CDC。重叠被容忍通过使应用幂等/upsert — 重放你已有的变化收敛到相同状态。

间隙 = 永远错过更新；这就是为什么"具有已知 offset 的快照"是承载细节。
