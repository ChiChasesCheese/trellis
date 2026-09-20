---
id: problems-metrics-monitoring-field-index-fanout-pruning
node: problems.search.metrics-monitoring
type: qa
step: 6
tags: [grown]
---
## Q
In a metrics monitoring system's query path, why does broadcasting every query to all storage leaf nodes stop scaling as the cluster grows, and how does a small label/field index at each zone and root level fix this without ever risking an incorrect result?

## A
A naive broadcast makes query cost scale with total cluster node count rather than with how selective the query's label predicates actually are, so even a narrow query touching one service's data still fans out to every leaf. A compact field index at each zone and at the root tracks approximately which leaves or zones could possibly hold a match for a given label predicate, and prunes candidates before the query fans out — Google's Monarch reports this cuts zone-level fan-out by about 99.5% and root-level fan-out by about 80%. Applying both rates to a topology of 20 zones × 500 leaves each (10,000 leaves total) collapses a query from touching all 10,000 leaves down to about 4 zones × 3 leaves ≈ 12, roughly an 833x reduction. The index is allowed to produce false positives (over-including a candidate) but never false negatives, because the actual leaf node still verifies the exact match — correctness never depends on the index being precise, only conservative.

## Q zh
在一个指标监控系统的查询路径中，为什么把每个查询广播给全部存储叶子节点会随集群增长而不可扩展？每个 zone 和 root 层级的一个小型标签/字段索引如何在不冒着返回错误结果的风险下解决这个问题？

## A zh
朴素广播让查询成本和集群总节点数挂钩，而不是和查询本身标签谓词的选择性挂钩，所以即使是只涉及一个服务数据的窄查询也要触达每一个叶子节点。每个 zone 和 root 各维护一个轻量字段索引，记录哪些叶子/zone 大致可能持有某个标签谓词的匹配，在查询真正扇出前做候选裁剪——Google 的 Monarch 披露这能把 zone 级扇出减少约 99.5%，root 级减少约 80%。把这两个比例套到一个 20 个 zone、每个 500 个叶子（共 10,000 个叶子）的拓扑上，查询从触达全部 10,000 个叶子降到约 4 个 zone × 3 个叶子 ≈ 12 个，降低约 833 倍。索引允许产生假阳性（多裁剪出不必要的候选），但绝不允许假阴性，因为真正的叶子节点仍会校验精确匹配——正确性从不依赖索引精确，只依赖它足够保守。
