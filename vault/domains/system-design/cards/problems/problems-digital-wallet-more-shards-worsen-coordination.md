---
id: problems-digital-wallet-more-shards-worsen-coordination
node: problems.commerce.digital-wallet
type: qa
step: 8
tags: [grown]
---
## Q
In a digital wallet scaling from 256 shards to 2,560 shards at 10x load, does adding shards reduce the number of transfers that need cross-shard coordination? What does change instead?

## A
No — the cross-shard fraction actually rises, from about 99.61% at 256 shards to about 99.96% at 2,560 shards, because the chance two random accounts collide onto the same shard shrinks as shard count grows. What changes at 10x scale is the absolute peak rate of cross-shard coordination calls (scaling with total transfer QPS, not shard count) and, if the transfer coordinator itself is single, whether it can be scaled horizontally as a stateless layer over a replicated decision log — sharding accounts more finely never substitutes for scaling the coordination path itself.

## Q zh
数字钱包从 256 个分片扩展到 2,560 个分片以应对 10 倍负载时，增加分片数量能减少需要跨分片协调的转账数量吗？真正变化的是什么？

## A zh
不能——跨分片比例反而会上升，从 256 个分片下约 99.61% 升到 2,560 个分片下约 99.96%，因为分片数越多，两个随机账户碰撞落在同一分片的概率就越小。10 倍规模下真正变化的是跨分片协调调用的绝对峰值速率（随转账总 QPS 而不是分片数扩展），以及——如果转账协调者本身是单一实例——它能否作为一个建立在复制决策日志之上的无状态层水平扩展；把账户分得更细，永远替代不了扩展协调路径本身。
