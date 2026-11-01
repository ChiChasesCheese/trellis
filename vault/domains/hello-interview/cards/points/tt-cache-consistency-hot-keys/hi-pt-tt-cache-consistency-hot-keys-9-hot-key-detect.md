---
id: hi-pt-tt-cache-consistency-hot-keys-9-hot-key-detect
node: tt.sd.tt-cache-consistency-hot-keys.points
type: qa
step: 9
---
## Q
**缓存一致性与热点 Key · 热 key 的发现**｜出自：缓存一致性与热点 Key › 深入 3

一个爆款占 100 万 QPS 的 20%（20 万 QPS）。为什么加机器没用？怎么发现热 key？

## A
**问题。** 缓存集群按 key 哈希分片，热 key 永远落在同一节点，网卡或 CPU 被打满并连累节点上的其他 key；加机器不会分散热点。
**发现。** 客户端 SDK 或代理层对每个 key 做滑动窗口计数，用 count-min sketch 加小顶堆维护 Top-K，超阈值（例如单实例每秒 1,000 次）上报；Redis LFU 统计作补充；大促商品提前人工标记。
