---
id: leetcode-c-snowflake-hyperloglog-application
node: topics.uncategorised
type: qa
anki: 1787365292981
tags: [algorithm::hashing, algorithm::hyperloglog, algorithm::mergeable-sketch, application, case, case::snowflake-hyperloglog, category::storage-databases, chapter::05, chapter::09, chapter::16, leetcode, system::snowflake]
---
## Q
Snowflake HyperLogLog 为什么能用固定小状态估算海量 distinct，并跨分片合并？

## A
它把 64-bit hash 分到 4096 个子流，每桶只记最大前导零长度，再从寄存器分布估算基数。两个状态的并集逐桶取 max；该操作满足交换律、结合律和幂等性，因此 worker 可先局部聚合，再用 HLL_COMBINE 合并。

**Evidence**

Snowflake 官方文档公开了 precision=12、4096 个子流、最多 4096-byte dense 状态及状态合并接口。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fstorage-databases%2FSnowflake%20HyperLogLog%EF%BC%9A%E5%9B%BA%E5%AE%9A%E7%8A%B6%E6%80%81%E7%9A%84%E8%BF%91%E4%BC%BC%E5%8E%BB%E9%87%8D)
