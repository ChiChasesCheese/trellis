---
id: uth-redis-compact-encodings-2-ziplist-cascade
node: redis.compact-encodings
type: qa
step: 2
---
## Q
**listpack 为什么取代 ziplist**｜Redis · 7.0 起

老的 ziplist 有什么毛病，让 Redis 7.0 把它换成了 listpack？

## A
**结构。** ziplist 的每个元素开头记“前一个元素的长度”（1 到 5 字节）；listpack 把长度挪到元素末尾，只记自己的长度。

**细节。**

- ziplist 在中间插入或删除元素，后一个元素的“前长度”可能从 1 字节变 5 字节
- 它自己也随之变长，再改变后面元素的前长度，一路连锁更新（cascade update）
- listpack 每个元素只依赖自己，没有连锁

**为什么。** 连锁更新让实现复杂、难审计；元素只用本地信息，代码更简单，倒着遍历依然成立。

**对应 LeetCode：** LC 707 设计链表 · LC 641 设计循环双端队列
