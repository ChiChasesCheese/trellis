---
id: distributed-lww-danger
node: distributed.time.clocks
type: qa
---
## Q
Why is last-write-wins by wall-clock timestamp a data-loss mechanism, not a conflict resolution strategy?

## A
Wall clocks on different nodes disagree: NTP sync leaves ms–100s of ms of skew, clocks **step backwards** on correction, and VMs pause. So "last" is decided by whichever node's clock runs fast — a genuinely later write can carry an *earlier* timestamp and be **silently discarded**. Cassandra-style LWW drops concurrent writes with no error and no trace.

Acceptable only when losing one of two concurrent updates is fine (e.g. idempotent "current status" values). Otherwise: version vectors to *detect* concurrency and merge, CRDTs, or route conflicting writes through a single leader. Hybrid: TrueTime-style bounded clocks (Spanner) make timestamp ordering safe by waiting out the uncertainty.

## Q zh
为什么按墙钟时间戳的 last-write-wins 是一种数据丢失机制，而不是冲突解决策略？

## A zh
不同节点上的墙钟并不一致：NTP 同步会留下几毫秒到上百毫秒的偏差，时钟在校正时会**向后跳变**，虚拟机还会暂停。所以"最后"是由哪个节点的时钟走得快来决定的——一次真正更晚的写入可能带着一个*更早*的时间戳，然后被**悄无声息地丢弃**。Cassandra 风格的 LWW 丢弃并发写入时既不报错也不留痕迹。

只有在丢失两个并发更新中的一个也无所谓的时候（例如幂等的"当前状态"值）才可以接受。否则就要用版本向量来*检测*并发再合并、用 CRDT，或者把冲突的写都路由经过单一 leader。折中方案：TrueTime 风格的有界时钟（Spanner）通过等出不确定区间，让时间戳排序变得安全。
