---
id: analytics-column-store-writes
node: analytics.olap
type: qa
---
## Q
Compressed sorted columns can't be updated in place. How do column stores accept writes anyway?

## A
The LSM move: writes land in a small **row-oriented (or unsorted) in-memory delta store**, and queries transparently merge the delta with the immutable, compressed column files. Background jobs periodically **rewrite/merge** deltas into new sorted column segments.

Consequences to know:
- Single-row updates/deletes are expensive relative to appends — column stores want **bulk, append-mostly** ingestion.
- A query is only fast again after merges keep the delta small; heavy trickle updates degrade scan performance.

Same amplification triangle as [[storage-amplification-triangle]], applied to analytics.

## Q zh
压缩排序列无法就地更新。列存储如何接受写入？

## A zh
LSM 移动：写入落地在小**行导向（或无序）内存 delta store**，查询透明地合并 delta 与不可变、压缩列文件。后台 job 定期**重写/合并** delta 到新的排序列 segment。

知道后果：
- 单行更新/删除相对追加是昂贵的 — 列存储想要**批量、追加最多**摄取。
- 查询仅在合并保持 delta 小后再快速；沉重的流水更新降低扫描性能。

与分析应用的相同放大三角。
