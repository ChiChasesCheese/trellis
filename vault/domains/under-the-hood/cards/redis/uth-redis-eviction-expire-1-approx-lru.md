---
id: uth-redis-eviction-expire-1-approx-lru
node: redis.eviction-expire
type: qa
step: 1
---
## Q
**Redis 的 LRU 为什么是“近似”的**｜Redis · 8.10

内存满了要淘汰最久没用的键，Redis 为什么不像 LeetCode 那样维护一条 LRU 链表？

## A
**结构。** 每个键只存一个 24 位的访问时间戳（精度 1 秒）；淘汰时随机采样，不维护全局顺序。

**细节。**

- 每轮随机抽 `maxmemory-samples` 个键，默认 5 个，上限 64
- 抽到的键放进 16 个位置的候选池（跨轮保留），淘汰空闲最久的
- 24 位秒级时间戳约 194 天回绕一次

**为什么。** 精确 LRU 要给每个键多存链表指针，每次读取还要挪节点；采样只花 3 字节，读时只写一个时间戳。

**对应 LeetCode：** LC 146 LRU 缓存 · LC 460 LFU 缓存
