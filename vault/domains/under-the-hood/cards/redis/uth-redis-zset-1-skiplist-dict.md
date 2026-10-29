---
id: uth-redis-zset-1-skiplist-dict
node: redis.zset
type: qa
step: 1
---
## Q
**有序集合为什么要存两份**｜Redis · 8.10

Redis 的 ZSET 底层是什么？`ZSCORE` 和 `ZRANGE` 为什么都很快？

## A
**结构。** 一张哈希表（成员 → 分数）加一个跳表（skip list，按分数排序），两者共用同一份成员字符串。

**细节。**

- 哈希表：`ZSCORE` 是 O(1)
- 跳表：插入、删除、范围查找平均 O(log n)，最底层是有序链表
- 节点随机分层：升一层的概率 P = 1/4，最多 32 层
- 条目不超过 128 个、每个不超过 64 字节时，改用 listpack

**为什么。** 只用哈希表没有顺序，只用跳表按成员找分数要 O(n)；两个结构各管一种查询。

**对应 LeetCode：** LC 1206 设计跳表 · LC 295 数据流的中位数
