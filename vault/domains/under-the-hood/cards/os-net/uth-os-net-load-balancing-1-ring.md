---
id: uth-os-net-load-balancing-1-ring
node: os-net.load-balancing
type: qa
step: 1
---
## Q
**一致性哈希环**｜Nginx · upstream hash consistent · 1.31

加一台后端时，怎样只搬走一小部分 key，而不像 `hash % N` 那样几乎全部重新洗牌？

## A
**结构。** 哈希环：每台服务器按权重在 2^32 的环上放 `160 × weight` 个虚拟节点（对主机、端口和上一个点的哈希做 crc32）；请求取 crc32 后，在排好序的点数组里二分，找第一个不小于它的点。

**细节。**

- 查找是 `ngx_http_upstream_find_chash_point` 里的二分，O(log 点数)
- 增删一台，只有它相邻区间的 key 换主，约 1/N 的 key 受影响
- 虚拟节点把每台机器的地盘切成许多小段，分布更均匀

**为什么。** `hash % N` 在 N 变化时几乎所有 key 都要重新映射，缓存全部失效；环把变动限制在被增删节点附近。

**对应 LeetCode：** LC 35 搜索插入位置 · LC 981 基于时间的键值存储
