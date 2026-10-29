---
id: uth-redis-compact-encodings-3-quicklist-intset
node: redis.compact-encodings
type: qa
step: 3
---
## Q
**List 和纯整数 Set 各用什么结构**｜Redis · 8.10

`LPUSH` 的 List 为什么不是一个长 listpack？只存整数的 Set 呢？

## A
**结构。** List 是 quicklist：双向链表，每个节点是一个 listpack。纯整数 Set 是 intset：有序的整数数组。

**细节。**

- quicklist 默认 `list-max-listpack-size = -2`：每个节点最多 8KB
- intset 用二分查找，元素按最小够用的宽度存：16、32 或 64 位
- 插入更大的数，整个数组升级到更宽编码，只升不降
- 整数 Set 不超过 512 个元素时用 intset

**为什么。** 一个超长 listpack 在中间插入要整体搬移；纯链表每个元素多两个指针；折中就是链表串起一段段小 listpack。

**对应 LeetCode：** LC 146 LRU 缓存 · LC 380 O(1) 时间插入、删除和获取随机元素
