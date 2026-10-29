---
id: uth-storage-buffer-pool-2-clock-sweep
node: storage.buffer-pool
type: qa
step: 2
---
## Q
**时钟扫描：近似 LRU，命中不挪节点**｜PostgreSQL · 18

PostgreSQL 的共享缓冲区（shared buffers）为什么不维护一条 LRU 链表？它怎么选被淘汰的页？

## A
**结构。** 缓冲区是固定数组，一个环形指针循环扫描；每个缓冲区有使用计数 `usage_count`，取值 0 到 5（`BM_MAX_USAGE_COUNT`）。

**细节。**

- 页每被使用一次，计数加 1，封顶 5。
- 淘汰指针扫过：被钉住（pin）的跳过；计数非 0 就减 1 继续走；遇到计数为 0 且没人用的，就是牺牲者。
- 最坏要扫 5 + 1 圈才能找到空位（源码注释）。

**为什么。** 命中只要改一个计数，不用像 LRU 链表那样把节点挪到表头；上限取得很大就逼近真 LRU，但扫的圈数也跟着变多。

**对应 LeetCode：** LC 146 LRU 缓存 · LC 460 LFU 缓存
