---
id: leetcode-c-postgresql-reservoir-sampling-application
node: topics.uncategorised
type: qa
anki: 1787361365298
tags: [algorithm::randomized-algorithm, algorithm::reservoir-sampling, algorithm::selectivity-estimation, application, case, case::postgresql-reservoir-sampling, category::storage-databases, chapter::09, chapter::10, leetcode, system::postgresql]
---
## Q
PostgreSQL ANALYZE 为什么适合 reservoir sampling？第 i 行被接纳的概率为什么是 k/i？

## A
扫描开始时不知道最终 n，又只能保留 k 行。第 i 行以 k/i 概率替换 reservoir 中随机一项；归纳后任意行在 n 行结束时保留概率都是 k/n。

**Evidence**

PostgreSQL 官方 ANALYZE 文档说明采样统计；analyze.c 实现固定目标样本的 acquisition 与 reservoir replacement。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fstorage-databases%2FPostgreSQL%20ANALYZE%EF%BC%9A%E8%93%84%E6%B0%B4%E6%B1%A0%E6%8A%BD%E6%A0%B7%E4%BC%B0%E8%AE%A1%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF)
