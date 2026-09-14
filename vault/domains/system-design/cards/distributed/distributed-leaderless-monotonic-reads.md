---
id: distributed-leaderless-monotonic-reads
node: distributed.replication.leaderless
type: qa
---
## Q
In a Dynamo-style store with W=2, R=2, N=3, a client reads a value and then reads it again and gets an *older* value. Explain how, and why the leader-based fix doesn't apply.

## A
A write reaches replicas one at a time. Read 1's coordinator happened to contact `{A, B}` where A had the new value; read 2's coordinator contacted `{B, C}` — neither of which was updated yet — so it legally returns the old one. Both quorums were valid; quorum overlap guarantees you *can* see the latest acknowledged write, not that you **stop** seeing it. That's a **monotonic reads** violation.

The leader-based fix — pin the session to one replica — doesn't work here because there is no fixed replica per key: **a different coordinator picks a different subset each request**, and any node can coordinate. Leaderless fixes instead:

- Have the client carry the **highest version it has seen** and reject/retry a quorum result older than it.
- Turn on **synchronous read repair** so a read that observes the new value pushes it to a write quorum before returning.

## Q zh
在一个 Dynamo 风格的存储中，W=2、R=2、N=3，一个客户端读到一个值，紧接着再读一次却得到了一个*更旧*的值。解释这是怎么发生的，以及为什么基于 leader 的修复方式在这里不适用。

## A zh
一次写会一个一个地到达各个副本。第一次读的协调者恰好联系了 `{A, B}`，其中 A 已经有了新值；第二次读的协调者联系的是 `{B, C}`——两者都还没被更新——于是合法地返回了旧值。两次 quorum 都是有效的；quorum 重叠保证的是你*可能*看到最新确认过的写入，而不是你**从此不再**看到旧值。这是一次**单调读（monotonic reads）**违反。

基于 leader 的修复方式——把会话固定到一个副本上——在这里不适用，因为这里不存在每个 key 固定的副本：**每次请求都由不同的协调者挑选不同的子集**，而且任何节点都可以充当协调者。无主系统改用别的修复方式：

- 让客户端携带它**见过的最高版本**，如果 quorum 结果比这个版本旧就拒绝/重试。
- 打开**同步 read repair**，让一次读到新值的操作在返回之前先把新值推送到一个写 quorum。
