---
id: analytics-join-strategies
node: analytics.batch
type: qa
---
## Q
Distributed join of a 10TB fact table with a 200MB dimension table: sort-merge join or broadcast hash join, and why?

## A
**Broadcast hash join**: ship the 200MB table to every executor, build an in-memory hash table, and stream the 10TB side through it — the big table never shuffles, and no sort is needed.

**Sort-merge join** is the fallback when *both* sides are large: shuffle both tables by join key so matching keys co-locate, sort each side, then merge. Cost: two full shuffles.

Rule: broadcast whenever one side fits comfortably in executor memory (engines auto-pick below a size threshold); if the "small" side is misestimated and doesn't fit, the join OOMs — a classic production failure.

## Q zh
10TB 事实表与 200MB 维度表的分布式 join：sort-merge join 还是 broadcast hash join，为什么？

## A zh
**Broadcast hash join**：把 200MB 表运送到每个 executor，构建内存 hash 表，通过它流 10TB 端 — 大表从不 shuffle，不需要排序。

**Sort-merge join** 是两端都大时的后备：按 join key shuffle 两个表，使匹配的 key 共址，排序每一端，然后合并。代价：两个完整 shuffle。

规则：当一端舒适地适合 executor 内存时广播（引擎自动在大小阈值下选择）；如果"小"端被误估且不适合，join OOM — 经典生产故障。
