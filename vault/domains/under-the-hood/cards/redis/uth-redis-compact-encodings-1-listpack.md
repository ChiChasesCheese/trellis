---
id: uth-redis-compact-encodings-1-listpack
node: redis.compact-encodings
type: qa
step: 1
---
## Q
**小哈希为什么不是哈希表**｜Redis · 8.10

只有几个字段的 Hash 或 ZSET，Redis 实际怎么存？

## A
**结构。** listpack：一整段连续内存，6 字节头部（总字节数 + 元素个数），后面依次排着元素。

**细节。**

- 每个元素 = 编码 + 数据 + 回溯长度（`backlen`），后者在元素末尾，所以能从尾往头倒着走
- 小整数只占 1 字节编码，短字符串只多 1 字节长度头
- 超过阈值才转成哈希表 / 跳表：Hash 默认 512 条，ZSET 默认 128 条，单个值超 64 字节也转

**为什么。** 元素少时，顺序扫一段连续内存比哈希表的指针、桶、节点更省内存，也更快。

**对应 LeetCode：** LC 705 设计哈希集合 · LC 706 设计哈希映射
