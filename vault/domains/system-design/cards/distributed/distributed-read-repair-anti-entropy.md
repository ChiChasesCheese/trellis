---
id: distributed-read-repair-anti-entropy
node: distributed.replication.leaderless
type: qa
---
## Q
In leaderless stores, read repair vs anti-entropy — how does each catch replicas up, and why do you need both?

## A
- **Read repair**: on a quorum read, the coordinator compares versions across replicas and writes the newest value back to any stale ones — repairs happen on the read path, so only **frequently-read** keys benefit.
- **Anti-entropy**: a background process diffs whole datasets between replicas (Merkle trees make the comparison cheap) and copies missing writes — covers **cold, never-read** data, but with no ordering and no freshness bound.

You need both because read repair alone leaves rarely-read data stale indefinitely — a *durability* hole: a value existing on only 1 of 3 replicas quietly waits for that replica's disk to die. (Hinted handoff is the third leg: replaying writes parked on stand-in nodes after a fault, see [[distributed-quorum-math]].)

## Q zh
在无主复制的存储中，read repair 和反熵——各自是怎样让副本追上进度的？为什么两个都需要？

## A zh
- **Read repair**：在一次 quorum 读中，协调者比较各副本的版本，把最新的值写回任何过时的副本——修复发生在读路径上，所以只有**经常被读**的 key 能受益。
- **反熵（anti-entropy）**：一个后台进程比较副本之间的整个数据集（Merkle 树让比较很便宜），把缺失的写拷贝过去——覆盖的是**冷的、从不被读**的数据，但没有顺序保证，也没有新鲜度上界。

两者都需要，是因为只靠 read repair 会让很少被读的数据无限期保持陈旧——这是一个*持久性*上的漏洞：一个只存在于 3 个副本中 1 个上的值，会悄悄地等着那个副本的磁盘坏掉。（Hinted handoff 是第三条腿：在故障之后，把暂存在替补节点上的写重放回去，参见 [[distributed-quorum-math]]。）
