---
id: uth-os-net-rate-limit-3-state
node: os-net.rate-limit
type: qa
step: 3
---
## Q
**限流的每个 IP 状态放哪里**｜Nginx · limit_req_zone · 1.31

给每个客户端记一份限流状态，几十万个 IP 怎么不撑爆内存？

## A
**结构。** 共享内存区里一棵红黑树（按 key 的哈希查找）加一条 LRU 队列（最近访问的挪到队头）。

**细节。**

- 每条状态占 64 字节（32 位平台）或 128 字节（64 位平台）；1 MB 的区能存约 8000 条 128 字节的状态
- 区满了，从队尾淘汰最久没访问的状态
- key 用 `$binary_remote_addr`（IPv4 只要 4 字节，IPv6 16 字节），比文本形式的 `$remote_addr` 省空间

**为什么。** 红黑树负责 O(log n) 查找，LRU 链表负责 O(1) 淘汰：就是 LRU 缓存的“哈希表加双向链表”，只是哈希表换成了红黑树。

**对应 LeetCode：** LC 146 LRU 缓存 · LC 729 我的日程安排表 I
