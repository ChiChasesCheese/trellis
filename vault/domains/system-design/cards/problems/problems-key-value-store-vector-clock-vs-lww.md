---
id: problems-key-value-store-vector-clock-vs-lww
node: problems.foundations.key-value-store
type: qa
step: 5
tags: [grown]
---
## Q
In a key-value store where sloppy quorums let two clients write the same key to different node subsets during a partition, why is last-write-wins by wall-clock timestamp dangerous, and what does using vector clocks trade away instead?

## A
Wall clocks on different nodes disagree, so a genuinely later write can carry an earlier timestamp and be silently discarded under LWW — unacceptable data loss for something like a shopping cart. Vector clocks instead attach a `{(node, counter), ...}` version to each write; if one version's counters all dominate another's, it's a clean successor and overwrites it, but if neither dominates, the writes are concurrent and both are kept as 'sibling' versions returned to the client to merge, since only the application knows how to merge business data. The trade is unbounded metadata growth: Dynamo bounds it by dropping the oldest (node, counter) pair once a threshold (the paper's example is 10) is reached, which can occasionally misjudge a true ancestor as concurrent, producing a harmless extra sibling.

## Q zh
在一个键值存储中，sloppy quorum 会让两个客户端在网络分区期间把同一个 key 写到不同的节点子集上，为什么按墙钟时间戳的 last-write-wins 很危险？用 vector clock 换来了什么代价？

## A zh
不同节点的墙钟本身就不一致，所以一次真正更晚的写入可能携带更早的时间戳，在 LWW 下被悄悄丢弃——对购物车这类场景是不可接受的数据丢失。Vector clock 则给每次写附加一个 `{(node, counter), ...}` 版本：如果一个版本的所有计数器都支配另一个版本，判定为干净的后继并覆盖；如果谁也不支配谁，判定为并发写入，两个版本都作为「兄弟版本」保留并返回给客户端合并，因为只有应用层才知道该怎么合并业务数据。代价是元数据可能无限增长：Dynamo 的做法是一旦分量数超过阈值（论文举例为 10）就丢弃最旧的 (node, counter) 分量，这偶尔会把一个真正的祖先版本误判成并发，产生一个无害但多余的兄弟版本。
