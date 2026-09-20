---
id: problems-auction-close-exactly-once-idempotent-token
node: problems.commerce.auction
type: qa
step: 6
tags: [grown]
---
## Q
Multiple scheduler instances (running for high availability) may all attempt to trigger the close of the same auction at roughly its end time. How does routing every close attempt through the same per-auction serialized actor, combined with a conditional write like `UPDATE auctions SET status='closed', close_token=:token WHERE id=:id AND status='active'`, guarantee the close side effects (declaring a winner, sending notifications) happen exactly once rather than zero or multiple times?

## A
Every scheduler instance's close attempt is routed to the same actor for that auction, so attempts are serialized rather than racing independently against the database. The conditional write only succeeds for the first attempt to reach the actor while status is still 'active' — it flips status to 'closed' and records a unique close_token in that same atomic operation. Every subsequent close attempt (from other scheduler instances, or from a retry) finds status already 'closed', so its conditional write matches zero rows, and the actor short-circuits: it returns 'already closed' without re-running the winner-declaration or notification logic, so those side effects never execute more than once.

## Q zh
多个调度器实例（为了高可用而并行运行）可能都在同一场拍卖的结束时间附近尝试触发关闭。为什么把每一次关闭尝试都路由到同一个按拍卖分区的序列化 actor，并配合一条条件写语句 `UPDATE auctions SET status='closed', close_token=:token WHERE id=:id AND status='active'`，能保证关闭的副作用（确定赢家、发送通知）恰好执行一次，而不是零次或多次？

## A zh
每个调度器实例针对同一场拍卖的关闭尝试都被路由到同一个 actor，所以这些尝试是被串行化的，而不是各自独立地和数据库竞争。条件写只有在 status 仍是“active”时到达 actor 的第一个尝试才会成功——它在同一个原子操作里把 status 改成“closed”并记录一个唯一的 close_token。之后的每一次关闭尝试（无论来自其他调度器实例还是重试）都会发现 status 已经是“closed”，它的条件写会匹配到零行，actor 直接短路返回“已经关闭”，不会重新执行确定赢家或发送通知的逻辑，所以这些副作用永远不会被执行超过一次。
