---
id: analytics-materialized-view-maintenance
node: analytics.derived
type: qa
---
## Q
A materialized view is stale the moment its base table changes. Compare the two maintenance strategies and when each wins.

## A
- **Full recompute on a schedule** (the classic warehouse/batch approach): simple, self-healing — every run erases previous errors — but freshness = schedule interval, and cost grows with base-table size regardless of how little changed.
- **Incremental maintenance**: consume the base table's changelog (CDC) and apply each change's *delta* to the view — a stream processor keeping a running aggregate. Fresh within seconds and cost proportional to change volume, but you now own streaming infrastructure, and non-decomposable logic (e.g. exact distinct counts, complex joins) needs real operator state, not just add/subtract.

Common hybrid: incremental for freshness + periodic full recompute to heal drift.

## Q zh
物化视图是其基表改变的时刻过时的。比较两个维护策略和各自何时胜出。

## A zh
- **在计划上完整重新计算**（经典 warehouse/batch 方法）：简单、自愈 — 每次运行消除前面的错误 — 但新鲜度 = 计划间隔，代价随基表大小增长不管改变了多少。
- **增量维护**：消费基表的 changelog（CDC）并应用每个变化的*delta*到视图 — stream processor 保持运行聚合。新鲜在秒内，代价与变化量成比例，但你现在拥有流基础设施，非可分解逻辑（例如精确 distinct 计数、复杂 join）需要真实 operator state，不仅仅加/减。

常见混合：增量用于新鲜度 + 定期完整重新计算来治愈 drift。
