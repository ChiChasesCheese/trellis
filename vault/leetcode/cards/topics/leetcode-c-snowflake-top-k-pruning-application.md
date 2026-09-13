---
id: leetcode-c-snowflake-top-k-pruning-application
node: topics.uncategorised
type: qa
anki: 1787365293180
tags: [algorithm::bounded-heap, algorithm::branch-and-bound, algorithm::top-k, application, case, case::snowflake-top-k-pruning, category::storage-databases, chapter::02, chapter::08, chapter::10, leetcode, system::snowflake]
---
## Q
为什么 `ORDER BY score DESC LIMIT K` 仍可能扫描全表？Snowflake Top-K pruning 何时能提前停？

## A
找到 K 行不等于证明它们是全局 top K。系统先维护当前第 K 大阈值 T；当它能证明所有剩余数据的乐观上界也不超过 T 时，剩余数据不可能改变答案，才可以停止扫描。

**Evidence**

Snowflake 官方文档说明，对满足条件的 ORDER BY + LIMIT 查询，系统可在确定剩余行无法进入 K 条结果时停止扫描。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fstorage-databases%2FSnowflake%20Top-K%20Pruning%EF%BC%9A%E6%9C%89%E7%95%8C%E7%AD%94%E6%A1%88%E4%B8%8E%E6%8F%90%E5%89%8D%E5%81%9C%E6%AD%A2)
