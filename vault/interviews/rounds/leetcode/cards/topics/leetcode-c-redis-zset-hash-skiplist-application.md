---
id: leetcode-c-redis-zset-hash-skiplist-application
node: topics.uncategorised
type: qa
anki: 1787359913492
tags: [algorithm::hash-table, algorithm::probabilistic-data-structure, algorithm::rank-query, algorithm::skip-list, application, case, case::redis-zset-hash-skiplist, category::storage-databases, leetcode, system::redis]
---
## Q
Redis Sorted Set 为什么同时维护 hash table 和 skip list？skip list 的 span 解决什么问题？

## A
hash table 让 member 到 score 的查询保持平均 O(1)；skip list 按 score/member 排序，支持期望 O(log N) 的插入、范围定位和有序遍历。每层 span 记录跨过的元素数，因此可以在跳跃查找时累计 rank。

**Evidence**

Redis 官方 t_zset.c 注释明确说明 zset 同时用 hash table 映射 object-to-score、用 skip list 维护 score order，并在 skiplist level 中维护 span。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fstorage-databases%2FRedis%20Sorted%20Set%EF%BC%9A%E5%93%88%E5%B8%8C%E8%A1%A8%E5%8A%A0%E8%B7%B3%E8%A1%A8)
