---
id: distributed-hot-key
node: distributed.partitioning.skew
type: qa
---
## Q
A celebrity account makes one partition take 100x the traffic of the rest. Why doesn't adding shards help, and what does?

## A
Adding shards rebalances *keys*, but all this load is on **one key** — it still lands on a single partition. Skew, not capacity, is the problem.

- **Reads**: cache the hot key in front (app/Redis tier, request coalescing) — reads are the easy half.
- **Writes**: **salt/split the key** — append a random suffix (`key#1..key#N`) to spread writes over N partitions; readers must fan out and merge, so apply only to detected hot keys.
- Isolate: move the hot key/tenant to its own dedicated partition or handling path.

Detection matters: per-key traffic metrics, because salting everything makes all reads scatter-gather.

## Q zh
一个明星账号让某个分区承受了其他分区 100 倍的流量。为什么加分片没用？什么才有用？

## A zh
加分片重新平衡的是*key*，但所有这些负载都压在**一个 key** 上——它还是会落到单个分区上。问题是倾斜，不是容量。

- **读**：在前面缓存这个热 key（应用层/Redis 层，请求合并）——读是简单的那一半。
- **写**：**给 key 加盐/拆分**——追加一个随机后缀（`key#1..key#N`）把写入分散到 N 个分区上；读的一方必须扇出后再合并，所以只对检测到的热 key 这样做。
- **隔离**：把这个热 key/租户挪到它自己专属的分区或处理路径上。

检测很关键：需要按 key 的流量指标，因为给所有 key 都加盐会让所有读都变成 scatter-gather。
