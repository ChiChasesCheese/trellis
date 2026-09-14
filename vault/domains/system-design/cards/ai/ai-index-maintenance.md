---
id: ai-index-maintenance
node: ai.vector-search
type: qa
---
## Q
Your vector index takes constant upserts and deletes. Why does incremental maintenance degrade HNSW over time, and when do you pay for a full rebuild?

## A
HNSW handles inserts well, but **deletes are tombstones**: the graph node is marked dead, not removed, so searches still traverse it — as the deleted fraction grows, latency rises and recall drops (dead nodes were routing shortcuts). IVF degrades differently: **centroids go stale** as the data distribution drifts, unbalancing lists and hurting recall.

Practice:

- Engines compact continuously (segment merges that drop tombstones, à la Lucene) — know your engine's mechanism.
- Trigger a **full rebuild** when tombstone ratio or recall-benchmark drift crosses a threshold, built **blue-green**: construct the new index alongside, backfill, dual-write during the build, cut reads over, drop the old.

Same cutover machinery serves embedding-model upgrades ([[ai-corpus-freshness]]).

## Q zh
您的向量索引执行持续的 upsert 和删除。为什么增量维护会随着时间推移而降级 HNSW，你何时需要支付完全重建的代价？

## A zh
HNSW 处理插入良好，但 **删除是墓碑**：图形节点被标记为死亡，而不是被移除，所以搜索仍然遍历它 — 随着删除部分增长，延迟上升，召回下降（死节点是路由快捷方式）。IVF 的降级方式不同：**质心变得过时** 因为数据分布漂移，不平衡列表并降低召回。

实践：

- 引擎持续紧凑（段合并删除墓碑，à la Lucene）— 了解你的引擎机制。
- 当墓碑比率或召回基准漂移超过阈值时触发 **完全重建**，构建 **蓝绿**：在旁边构建新索引，回填，在构建期间双写，切割读取，放弃旧的。

相同的切换机制服务 embedding 模型升级（[[ai-corpus-freshness]]）。
