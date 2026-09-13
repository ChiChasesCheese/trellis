---
id: leetcode-c-snowflake-micro-partition-pruning-application
node: topics.uncategorised
type: qa
anki: 1787365293081
tags: [algorithm::columnar-storage, algorithm::interval-pruning, algorithm::min-max-index, application, case, case::snowflake-micro-partition-pruning, category::storage-databases, chapter::02, chapter::08, chapter::10, leetcode, system::snowflake]
---
## Q
Snowflake micro-partition pruning 的核心判定是什么？为什么有 min/max 仍可能扫全表？

## A
优化器用谓词区间与分区列值域做保守判空：能证明不相交才跳过，否则必须扫描。若数据分布混乱，使大量分区的 min/max 范围互相重叠，元数据虽然正确却缺乏区分度，因此仍可能扫描大部分分区。

**Evidence**

Snowflake 官方文档说明 micro-partition 保存列值域等元数据，并用这些元数据在查询时进行分区和列 pruning。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fstorage-databases%2FSnowflake%20Micro-partition%20Pruning%EF%BC%9AMin-Max%20%E5%85%83%E6%95%B0%E6%8D%AE%E4%B8%8E%E5%8C%BA%E9%97%B4%E5%89%AA%E6%9E%9D)
