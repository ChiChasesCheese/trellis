---
id: problems-tinder-swipe-write-forces-wide-column
node: problems.social.tinder
type: qa
step: 1
tags: [grown]
---
## Q
In a Tinder-style dating app design with 10 million daily active users each swiping 150 times/day on average, the computed peak swipe-write QPS is about 52,083. If a single relational primary is assumed to sustain a few thousand conditional updates/sec (roughly 3,000/sec), what does the ratio between these two numbers force in the write path's storage choice?

## A
52,083 / 3,000 ≈ 17.4x over the assumed relational primary's ceiling, so a single relational database cannot absorb the swipe-write peak. This forces swipe writes onto a wide-column store (Cassandra-class) partitioned by the swiping user's id, since the write pattern is a simple per-user append that never needs a cross-user transaction, and the store's write-optimized engine can scale horizontally by adding more partitions rather than scaling up one primary.

## Q zh
在一个 Tinder 式约会应用设计里，1000 万日活用户平均每天滑动 150 次，算出的峰值滑动写入 QPS 约为 52,083。如果假设单个关系型主库在简单条件更新下的承受能力是几千次/秒（约 3,000/秒），这两个数字之间的比例对写路径的存储选型意味着什么？

## A zh
52,083 / 3,000 ≈ 17.4 倍，超出假设的关系型主库上限约 17.4 倍，单个关系型数据库无法承受这个滑动写入峰值。这迫使滑动写入转向按滑动者 id 分区的宽列存储（Cassandra 一类）——因为写入模式是简单的按用户追加写，从不需要跨用户事务，宽列存储的写优化引擎可以通过增加分区水平扩展，而不是靠单一主库垂直扩容。
