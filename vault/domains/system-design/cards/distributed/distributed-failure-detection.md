---
id: distributed-failure-detection
node: distributed.time.failure
type: qa
---
## Q
Why can no timeout prove a remote node is dead, and how do real systems pick and use timeouts anyway?

## A
In an asynchronous network you can't distinguish **crashed** from **slow / partitioned / GC-paused**: no reply within T is consistent with all of them, and the node may resume and keep acting (why fencing exists).

Practice:
- Pick T from **observed latency distributions** (e.g. p999 × margin), not a folklore constant; adaptive detectors like **phi-accrual** (Cassandra/Akka) output a suspicion level from the heartbeat history instead of a binary verdict.
- Make the *reaction* safe rather than the detection perfect: quorum-agreed membership, leases that must expire before takeover, fencing on the resource.

Trade-off to state: short timeout = fast failover but false positives (flapping, duplicate leaders' work); long timeout = slow recovery.

## Q zh
为什么没有任何超时能证明一个远端节点真的死了？现实中的系统究竟怎样选择和使用超时？

## A zh
在一个异步网络里，你无法区分**已崩溃**和**慢/被分区/GC 暂停**：T 时间内没有回应，这几种情况都符合，而且那个节点可能会恢复并继续行动（这正是 fencing 存在的原因）。

实践做法：
- 从**观测到的延迟分布**（例如 p999 × 一个余量）里选 T，而不是拍脑袋定一个常量；像 **phi-accrual**（Cassandra/Akka）这样的自适应检测器根据心跳历史输出一个怀疑度，而不是一个二元判断。
- 让*反应*本身是安全的，而不是追求检测的完美：由 quorum 达成一致的成员关系、接管前必须先过期的租约、对资源做 fencing。

要说清楚的权衡：超时短 = 故障转移快但容易误报（抖动、重复的 leader 各自干活）；超时长 = 恢复慢。
