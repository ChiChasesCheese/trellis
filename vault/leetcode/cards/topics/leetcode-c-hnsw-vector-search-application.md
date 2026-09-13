---
id: leetcode-c-hnsw-vector-search-application
node: topics.uncategorised
type: qa
anki: 1787365291105
tags: [algorithm::approximate-nearest-neighbor, algorithm::best-first-search, algorithm::bounded-heap, algorithm::small-world-graph, application, case, case::hnsw-vector-search, category::developer-infrastructure, chapter::06, chapter::08, chapter::10, leetcode, system::faiss, system::hnsw, system::vector-database]
---
## Q
HNSW 为什么要分层？`M`、`efConstruction`、`efSearch` 分别交换什么资源？

## A
稀疏高层提供长距离导航，稠密底层用 best-first candidate search 精炼，避免从坏入口在单层图里走太久。M 用内存换连接与 recall；efConstruction 用建图时间换图质量；efSearch 用查询距离计算和延迟换 recall。

**Evidence**

HNSW 原论文定义分层 navigable small-world graph；Faiss 官方文档公开 M、efConstruction、efSearch 的内存/准确率/速度权衡。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdeveloper-infrastructure%2FHNSW%20%E5%90%91%E9%87%8F%E6%A3%80%E7%B4%A2%EF%BC%9A%E5%88%86%E5%B1%82%E5%B0%8F%E4%B8%96%E7%95%8C%E5%9B%BE%E4%B8%8E%E5%80%99%E9%80%89%E5%A0%86)
