---
id: problems-ride-hailing-exclusive-lock-not-optimistic
node: problems.geo.ride-hailing
type: qa
step: 2
tags: [grown]
---
## Q
In a ride-hailing matching service, two riders in the same sparse area can both have the same driver selected as their top candidate at nearly the same instant. Why does this design use an explicit short-TTL exclusive lock on the driver before sending an invitation, instead of optimistic concurrency (match both, detect the conflict, retry the loser)?

## A
Optimistic concurrency assumes conflicts are rare and a losing retry is cheap, but here the cost is asymmetric: once an invitation has actually been pushed to the driver's app, a conflict is no longer an invisible internal retry — the driver would receive two contradictory ride invitations that the user directly experiences as a bug. The design instead locks the driver_id with a short TTL (a few seconds, covering the longest reasonable response time) before sending any invitation; a failed lock attempt means another matching flow already holds it, so the service immediately moves to the next candidate rather than waiting, and the short TTL guarantees the lock releases automatically if the driver never responds or the client crashes, instead of depending on an explicit release that might never arrive.

## Q zh
在一个网约车撮合服务中，同一片稀疏区域里的两个乘客几乎在同一时刻都可能把同一个司机选为各自的首选候选人。为什么这个设计在发邀请之前先对该司机加一把短 TTL 排他锁，而不是用乐观并发（先各自撮合，检测到冲突后重试落败的一方）？

## A zh
乐观并发的前提是冲突很少见、落败方重试的代价可以接受，但这里代价是不对称的：一旦邀请已经真的推送到司机的 App 上，冲突就不再是一个不可见的内部重试，而是司机会收到两条互相矛盾的邀请，用户能直接感知到这是一个错误。这个设计改为在发任何邀请之前，先对 driver_id 加一把 TTL 很短（几秒，覆盖合理的最长响应时间）的锁；加锁失败说明另一个撮合流程已经持有它，服务立刻转向下一个候选人而不是等待，而短 TTL 保证了即使司机永远不响应或客户端崩溃，锁也会自动释放，而不依赖一个可能永远不会到达的显式释放信号。
