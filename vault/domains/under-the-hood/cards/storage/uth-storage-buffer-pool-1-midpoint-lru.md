---
id: uth-storage-buffer-pool-1-midpoint-lru
node: storage.buffer-pool
type: qa
step: 1
---
## Q
**中点 LRU：扫描不冲掉热页**｜InnoDB · MySQL 8.4

一条全表扫描读了几十 GB，为什么没有把缓冲池里的热页挤光？

## A
**结构。** 缓冲池是一条 LRU 链表，分成前面的新（young）段和后面的老（old）段。老段占 3/8（`innodb_old_blocks_pct` 默认 37）。

**细节。**

- 新读入的页插在中点，即老段的头。
- 老段里的页再次被访问时，要距第一次访问已过 `innodb_old_blocks_time`（默认 1000 ms）才晋升到新段的头。
- 扫描会连续访问同一页，这些访问不算数，扫完就沉到老段尾部淘汰。

**为什么。** 纯 LRU 下，扫描读进来的每一页都成了“最近使用”；有了中点和时间门槛，才分得出一次性访问和真正的热点。

**对应 LeetCode：** LC 146 LRU 缓存 · LC 460 LFU 缓存
