---
id: attrib-join-access-history-tables
node: cost.access-history-lineage-for-cost
type: qa
tags: [grown]
---
## Q
如何找出“是哪些表在驱动计算支出”，从而判断该给哪张表加聚簇键或物化？

## A
把每条查询的计算成本与它读取的表关联：从 `QUERY_ATTRIBUTION_HISTORY`（或 `QUERY_HISTORY` 的耗时、扫描字节）取得每个 query_id 的成本，与 `ACCESS_HISTORY` 中 `BASE_OBJECTS_ACCESSED` 展开出的底层表按 query_id 连接，再按表汇总成本（一条查询读多张表时需按规则分摊）。使用底层对象而不是直接对象，是为了让通过视图访问的查询也把成本记到真正被扫描的表上。
