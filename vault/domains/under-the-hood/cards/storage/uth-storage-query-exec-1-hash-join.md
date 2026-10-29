---
id: uth-storage-query-exec-1-hash-join
node: storage.query-exec
type: qa
step: 1
---
## Q
**哈希连接 = 两数之和**｜PostgreSQL · 18

`orders JOIN users ON orders.uid = users.id` 没有合适索引时，PostgreSQL 怎么连接？表大到内存放不下呢？

## A
**结构。** 哈希连接（hash join）：先扫较小的那张表（内表）在内存里建哈希表，再逐行扫另一张表去探测（probe）。

**细节。**

- 内存上限 = `work_mem`（默认 4 MB）× `hash_mem_multiplier`（15 起默认 2.0，14 及之前 1.0），即默认 8 MB。
- 放不下就分批（batch）：两张表按哈希值分到临时文件，一批一批地连。批数总是 2 的幂，发现某批太大就翻倍。

**为什么。** 复杂度 O(n + m)，嵌套循环是 O(n × m)；代价是只能做等值连接。

**对应 LeetCode：** LC 1 两数之和 · LC 349 两个数组的交集
