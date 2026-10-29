---
id: uth-redis-sds-dict-1-sds
node: redis.sds-dict
type: qa
step: 1
---
## Q
**Redis 为什么不用 C 字符串**｜Redis · 8.10

Redis 的字符串底层 SDS（Simple Dynamic String）和 C 的 `char*` 比，多了什么？

## A
**结构。** 一段连续内存，头部存 `len`（已用）、`alloc`（容量）、`flags`（类型），指针指向头部之后的字符数据。

**细节。**

- 头部按长度分 5 种，长度字段最小 1 字节，最大 8 字节
- 追加时预分配：新长度小于 1MB 就翻倍，否则每次多给 1MB
- 长度 O(1) 读出，内容里可以有 `\0`（二进制安全）

**为什么。** C 字符串求长度要扫一遍，追加要反复 `realloc`；多几个字节的头部换来 O(1) 求长和均摊 O(1) 追加。

**对应 LeetCode：** LC 380 O(1) 时间插入、删除和获取随机元素 · LC 155 最小栈
