---
id: distributed-sloppy-quorum-handoff
node: distributed.replication.leaderless
type: qa
---
## Q
Trace a write under a sloppy quorum with hinted handoff: where does it land, when does it get home, and what are the two ways it never gets there?

## A
The key's N home replicas are decided by the ring. If some are unreachable, the coordinator writes to the **first N reachable nodes instead**, and a stand-in stores the value in a separate **hint** — a durable record tagged "this belongs to node 7". When node 7 is seen alive again (gossip), the stand-in **replays the hints to it** and deletes them.

It never gets home when:

- **The hint window expires** — hints are only retained for a bounded time (Cassandra's `max_hint_window`, hours by default); after that they are dropped and only anti-entropy repair can fix the replica.
- **The stand-in dies** before replaying, taking the only copy of the hint with it.

Hence the guarantee downgrade: a sloppy write is a **durability/availability boost, not a quorum** — the R read replicas need not intersect the nodes that actually took the write, so `W + R > N` no longer implies you read it back.

## Q zh
追踪一次在 sloppy quorum 加 hinted handoff 下的写入：它落在哪里？什么时候能回到家？又有哪两种方式让它永远回不去？

## A zh
一个 key 的 N 个归属副本由环决定。如果其中一些不可达，协调者就转而写入**前 N 个可达的节点**，而某个替补节点会把这个值存进一份单独的**hint**里——一条标记着"这属于节点 7"的持久记录。当节点 7 重新被看到存活（通过 gossip）时，替补节点会把 **hint 重放给它**，然后删除这些 hint。

它永远回不去的两种情况：

- **hint 窗口过期**——hint 只保留一段有限的时间（Cassandra 的 `max_hint_window`，默认几个小时）；过了这个时间就会被丢弃，只有反熵修复才能修好那个副本了。
- **替补节点在重放之前就挂了**，把 hint 的唯一副本一起带走了。

因此这个保证是被降级的：一次 sloppy 写只是**持久性/可用性上的加成，不是一次 quorum**——R 个读副本不需要和真正接受了这次写的节点相交，所以 `W + R > N` 不再意味着你能读回这次写入。
