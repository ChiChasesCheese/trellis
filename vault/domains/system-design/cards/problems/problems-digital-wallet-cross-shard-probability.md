---
id: problems-digital-wallet-cross-shard-probability
node: problems.commerce.digital-wallet
type: qa
step: 1
tags: [grown]
---
## Q
In a digital wallet design where accounts are hashed across 256 shards by account id, what fraction of wallet-to-wallet transfers are cross-shard, and why does adding more shards make this worse rather than better?

## A
With 256 shards and uniform hashing, the probability two independent accounts land on the same shard is 1/256 ≈ 0.39%, so about 99.61% of transfers cross a shard boundary. Adding shards to handle more load raises this fraction further — at 2,560 shards it rises to about 99.96% — because the odds of two random accounts colliding on one shard shrink as shard count grows. This means cross-shard coordination must be treated as the default transfer path from day one, not a rare case optimized later; more sharding never reduces the need for it.

## Q zh
在一个按 account id 哈希分成 256 个分片的数字钱包设计中，钱包间转账有多大比例是跨分片的？为什么增加分片数量会让这个比例变得更高而不是更低？

## A zh
在 256 个分片、均匀哈希分布下，两个独立账户落在同一分片的概率是 1/256 ≈ 0.39%，因此约 99.61% 的转账会跨越分片边界。为了承载更多负载而增加分片数量，会让这个比例进一步升高——分到 2,560 个分片时升至约 99.96%，因为分片数越多，两个随机账户碰撞在同一分片的概率就越小。这意味着跨分片协调必须从第一天起就是转账的默认路径，而不是后期才优化的边缘情况；分片越多，越离不开跨分片协调。
