---
id: reliability-active-active-vs-passive
node: reliability.multi-region
type: qa
---
## Q
When is active-passive the right multi-region design over active-active, given that active-active looks strictly better on paper?

## A
Choose **active-passive** when writes must stay strongly consistent and single-homed: one region owns all writes, so there are no cross-region write conflicts and no conflict-resolution logic — at the cost of higher write latency for far users and a real failover event.

**Active-active** serves writes in every region (great latency, region loss is a non-event) but forces you to handle **concurrent conflicting writes** — CRDTs, last-writer-wins, or partitioning users to a home region. If your domain can't tolerate merge semantics (payments, inventory), active-active on the write path is the wrong call.

## Q zh
在 active-active 看起来明显更优的情况下，什么时候应该用 active-passive 的多区域设计？

## A zh
选择 **active-passive** 当写操作必须保证强一致性且单一源点：一个区域拥有所有写操作，因此没有跨区域写冲突，也不需要冲突解决逻辑——代价是远端用户的写入延迟更高，需要真正的故障转移事件。

**Active-active** 在每个区域都能处理写操作（对延迟很好，区域丢失不是个事件），但强制你处理**并发冲突写**——CRDT、last-writer-wins 或把用户分片到主区域。如果你的业务域无法容忍合并语义（支付、库存），active-active 在写入路径上就是错误的选择。
