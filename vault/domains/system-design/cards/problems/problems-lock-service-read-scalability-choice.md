---
id: problems-lock-service-read-scalability-choice
node: problems.foundations.lock-service
type: qa
step: 6
tags: [grown]
---
## Q
In a distributed lock/coordination service design, why should a client's read of 'roughly who the current leader is, for routing purposes' be served as a serializable (possibly stale) local read from a follower, while a read used to verify 'do I still hold this lock right now' before performing a fencing-token-guarded write must be linearizable?

## A
The two reads differ in what happens if the answer is stale. A routing read that returns a slightly outdated leader just causes the client to be redirected once it hits the wrong node — a cheap, self-correcting failure with an existing retry path. A safety-verification read feeding into a decision that a downstream resource will trust (via its fencing-token check) has no such correction mechanism: if it returns stale data, the client may proceed to write believing it still holds the lock when it does not, defeating the whole point of the token check. Routing reads should therefore default to cheap serializable local reads to spread load off the leader, while safety-critical reads must pay for a linearizable read (e.g. read index) even though it costs a quorum round trip.

## Q zh
在一个分布式锁/协调服务设计中，为什么客户端读取「大概谁是当前 leader，用来决定路由」这种查询应该走可串行化（可能稍旧）的 follower 本地读，而在执行一次受 fencing token 保护的写之前用来确认「我现在是否仍然持有这把锁」的读，却必须是线性一致的？

## A zh
这两种读的区别在于结果陈旧时会发生什么。一次路由读即使返回了稍旧的 leader 信息，后果也只是客户端打到了错误的节点后被重定向一次——代价很低，而且有现成的重试路径自我纠正。而一次接入安全校验决策的读（下游资源会信任它做出的 fencing-token 判断）没有这种纠正机制：如果它返回了陈旧数据，客户端可能会带着「我仍然持有这把锁」的错误信念继续写下去，这就彻底破坏了令牌校验本来要防止的事情。因此路由类的读应该默认走廉价的可串行化本地读、把负载从 leader 上分摊出去，而安全校验类的读必须付出线性一致读（例如 read index）的代价，即使这意味着一次 quorum 往返。
