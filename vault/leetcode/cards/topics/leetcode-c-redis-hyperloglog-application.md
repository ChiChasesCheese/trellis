---
id: leetcode-c-redis-hyperloglog-application
node: topics.uncategorised
type: qa
anki: 1787361365822
tags: [algorithm::hashing, algorithm::hyperloglog, algorithm::probabilistic-counting, application, case, case::redis-hyperloglog, category::storage-databases, chapter::09, leetcode, system::redis]
---
## Q
Redis HyperLogLog 为什么能合并两个计数器，却不能删除一个 member？

## A
合并只需对同位置 registers 取 max；register 保存的是历史极值，不知道哪个 member 贡献了该极值，所以删除单个 member 无法恢复次大值。

**Evidence**

Redis 官方 HLL 文档与原始论文定义 register、误差、PFMERGE 和基数估计。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fstorage-databases%2FRedis%20HyperLogLog%EF%BC%9A%E6%A6%82%E7%8E%87%E8%AE%A1%E6%95%B0%E4%B8%8E%E8%B0%83%E5%92%8C%E5%B9%B3%E5%9D%87)
